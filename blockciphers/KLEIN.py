#! /usr/bin/env python

SBOX = [0x7, 0x4, 0xA, 0x9, 0x1, 0xF, 0xB, 0x0,
        0xC, 0x3, 0x2, 0x6, 0x8, 0xE, 0xD, 0x5]

class KLEIN(object):

    def __init__(self, nr=12, size=64):
        self.nr = nr
        self.size = size

    def addRoundKey(self, state, sk):
        pass

    def subNibbles(self, state):
        pass

    def rotateNibbles(self, state):
        pass

    def mixNibbles(self, state):
        pass

    def keySchedule(self, sk, i):
        pass

    def encrypt(self, plaintext, key, nr=12, size=64):
        state = plaintext
        sk = key
        for i in range(nr):
            state = self.addRoundKey(state, sk)
            state = self.subNibbles(state)
            state = self.rotateNibbles(state)
            state = self.mixNibbles(state)
            sk = self.keySchedule(sk, i)
        state = self.addRoundKey(state, sk)
        return state
