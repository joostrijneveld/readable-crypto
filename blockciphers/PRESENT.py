#! /usr/bin/env python

SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

class PRESENT(object):

    def __init__(self, size=80):
        self.size = size

    def addRoundKey(self, state, rk):
        return state ^ rk

    def sBoxlayer(self, state):
        for i in range(0, 64, 4):
            word = (state >> i) & 0xF
            state = state & ~(0xF << i) | (SBOX[word] << i)
        return state

    def pLayer(self, state):
        P = ( 0, 16, 32, 48,  1, 17, 33, 49,  2, 18, 34, 50,  3, 19, 35, 51,
              4, 20, 36, 52,  5, 21, 37, 53,  6, 22, 38, 54,  7, 23, 39, 55,
              8, 24, 40, 56,  9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
             12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63)
        oldstate = state
        for i, j in enumerate(P):
            state = state & ~(0x1 << j) | ((oldstate >> i) & 0x1) << j
        return state

    def keySchedule(self, K, i):
        K = (K << 61) & int('1' * self.size, 2) | K >> self.size-61
        if self.size == 80:
            word = (K >> 76) & 0xF
            K = K & ~(0xF << 76) | (SBOX[word] << 76)
            K ^= i << 15
        elif self.size == 128:
            words = (K >> 120) & 0xFF
            K &= ~(0xFF << 120)
            K |= (SBOX[words >> 4] << 124)
            K |= (SBOX[words & 0xF] << 120)
            K ^= i << 62
        return K

    def encrypt(self, plaintext, key):
        state = plaintext
        K = key
        for i in range(1, 32):
            rk = K >> (self.size-64)
            state = self.addRoundKey(state, rk)
            state = self.sBoxlayer(state)
            state = self.pLayer(state)
            K = self.keySchedule(K, i)
        rk = K >> (self.size-64)
        state = self.addRoundKey(state, rk)
        return state
