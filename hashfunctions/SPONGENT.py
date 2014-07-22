#! /usr/bin/env python

import math

SBOX = [0xE, 0xD, 0xB, 0x0, 0x2, 0x1, 0x4, 0xF,
        0x7, 0xA, 0x8, 0x5, 0x9, 0xC, 0x3, 0x6]


class SPONGENT(object):

    def __init__(self, n=88, c=80, r=8, R=45):
        self.n = n
        self.c = c
        self.r = r
        self.R = R
        self.LFSRsize = math.ceil(math.log2(R))
        self.LFSRmask = int('1' * self.LFSRsize, 2)
        self.reset_LFSR()

    def initialise(self, m, prefix_zeros=0):
        m = m << 1 | 1
        length = len(bin(m)) - 2 + prefix_zeros  # -2 for 0b prefix
        m <<= self.r - length % self.r
        N = math.ceil((prefix_zeros + length) / self.r)
        return m, N

    def sBoxLayer(self, state):
        for i in range(0, (self.r + self.c), 4):
            word = (state >> i) & 0xF
            state = state & ~(0xF << i) | (SBOX[word] << i)
        return state

    def pLayer(self, state):
        b = self.r + self.c

        def Pb(j):
            if j <= b - 2:
                return (j * b//4) % (b - 1)
            return b - 1

        oldstate = state
        for j in range(b):
            state = state & ~(0x1 << Pb(j)) | ((oldstate >> j) & 0x1) << Pb(j)
        return state

    def reset_LFSR(self):
        self.LFSR = {88:  int('000101', 2),
                     128: int('1111010', 2),
                     160: int('1000101', 2),
                     224: int('0000001', 2),
                     256: int('10011110', 2)}[self.n]

    def lCounter(self):
        z = lambda i: (self.LFSR >> i-1) & 0x1
        if self.n == 88:
            x = z(6) ^ z(5)
        elif self.n in [128, 160, 224]:
            x = z(7) ^ z(6)
        elif self.n == 256:
            x = z(8) ^ z(4) ^ z(3) ^ z(2)
        self.LFSR = (self.LFSR << 1 | x) & self.LFSRmask

    def P(self, s):
        self.reset_LFSR()
        for _ in range(1, self.R+1):
            tmp = self.LFSR
            revLFSR = 0
            for _ in range(self.LFSRsize):
                revLFSR = revLFSR << 1 | tmp & 0x1
                tmp >>= 1
            s = (revLFSR << (self.r + self.c - self.LFSRsize)) ^ s ^ self.LFSR
            self.lCounter()
            s = self.sBoxLayer(s)
            s = self.pLayer(s)
        return s

    # The necessity of this function is not clear in the SPONGENT article
    # It follows from the test vectors produced by the reference implementation
    # The message blocks are reversed on a per-byte basis; this shows for r > 8
    def reverse_block(self, block):
        result = 0
        for _ in range(self.r//8):
            result = result << 8 | block & 0xFF
            block >>= 8
        return result

    def absorb(self, m, N):
        mblocks = []
        for i in range(N):
            mblocks.append(m & int('1' * self.r, 2))
            m >>= self.r
        s = 0
        for mblock in reversed(mblocks):
            s = s ^ self.reverse_block(mblock)
            s = self.P(s)
        return s

    def squeeze(self, s):
        result = 0x0
        for i in range(self.n // self.r - 1):
            result = result | self.reverse_block(s & int('1' * self.r, 2))
            result <<= self.r
            s = self.P(s)
        result = result | self.reverse_block(s & int('1' * self.r, 2))
        return result

    def hash(self, m, prefix_zeros=0):
        m, N = self.initialise(m, prefix_zeros)
        s = self.absorb(m, N)
        return self.squeeze(s)
