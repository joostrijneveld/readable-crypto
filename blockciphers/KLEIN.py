#! /usr/bin/env python

SBOX = [0x7, 0x4, 0xA, 0x9, 0x1, 0xF, 0xB, 0x0,
        0xC, 0x3, 0x2, 0x6, 0x8, 0xE, 0xD, 0x5]


def sbox_nibble(bits, i, N):
    """Replaces the i-th nibble (0-base) in N bits with SBOX[nibble]."""
    offset = N - (i+1)*4
    nibble = (bits >> offset) & 0xF  # fetch the nibble
    return bits & ~(0xF << offset) | (SBOX[nibble] << offset)  # add back in

class KLEIN(object):

    def __init__(self, nr=12, size=64):
        self.nr = nr
        self.size = size

    def addRoundKey(self, state, sk):
        return state ^ (sk >> self.size-64) & 0xFFFFFFFFFFFFFFFF

    def subNibbles(self, state):
        for i in range(16):
            state = sbox_nibble(state, i, 64)
        return state

    def rotateNibbles(self, state):
        return (state << 16) & 0xFFFFFFFFFFFFFFFF | (state >> 48)

    def mixNibbles(self, state):
        def mix_columns(bits):
            c01 = 0xFF & (bits >> 24)
            c23 = 0xFF & (bits >> 16)
            c45 = 0xFF & (bits >> 8)
            c67 = 0xFF & bits

            def mul2or3(x, n):  # this is not nearly as generic as galoisMult
                x = (x << 1) if n == 2 else ((x << 1) ^ x)
                if x > 0xFF:
                    return (x ^ 0x1B) & 0xFF
                return x

            s01 = mul2or3(c01, 2) ^ mul2or3(c23, 3) ^ c45 ^ c67
            s23 = c01 ^ mul2or3(c23, 2) ^ mul2or3(c45, 3) ^ c67
            s45 = c01 ^ c23 ^ mul2or3(c45, 2) ^ mul2or3(c67, 3)
            s67 = mul2or3(c01, 3) ^ c23 ^ c45 ^ mul2or3(c67, 2)
            return s01 << 24 | s23 << 16 | s45 << 8 | s67

        col1 = mix_columns(state >> 32)
        col2 = mix_columns(state & 0xFFFFFFFFFFFFFFFF)
        return col1 << 32 | col2

    def keySchedule(self, sk, i):
        a = (sk >> self.size//2)
        b = sk & int('1' * (self.size//2), 2)
        a = (a << 8) & int('1' * (self.size//2), 2) | (a >> (self.size//2 - 8))
        b = (b << 8) & int('1' * (self.size//2), 2) | (b >> (self.size//2 - 8))
        a ^= b
        a, b = b, a
        a ^= i << (self.size//2 - 24)
        for i in range(2, 6):
            b = sbox_nibble(b, i, self.size//2)
        return a << self.size//2 | b

    def encrypt(self, key, plaintext):
        state = plaintext
        sk = key
        for i in range(1, self.nr+1):
            state = self.addRoundKey(state, sk)
            state = self.subNibbles(state)
            state = self.rotateNibbles(state)
            state = self.mixNibbles(state)
            sk = self.keySchedule(sk, i)
        state = self.addRoundKey(state, sk)
        return state
