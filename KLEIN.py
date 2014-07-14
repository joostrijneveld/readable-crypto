#! /usr/bin/env python

SBOX = [0x7, 0x4, 0xA, 0x9, 0x1, 0xF, 0xB, 0x0,
        0xC, 0x3, 0x2, 0x6, 0x8, 0xE, 0xD, 0x5]

def addRoundKey(state, sk):
    pass

def subNibbles(state):
    pass

def rotateNibbles(state):
    pass

def mixNibbles(state):
    pass
    
def keySchedule(sk, i):
    pass

def encrypt(plaintext, key, nr=12, size=64):
    state = plaintext
    sk = key
    for i in range(nr):
        state = addRoundKey(state, sk)
        state = subNibbles(state)
        state = rotateNibbles(state)
        state = mixNibbles(state)
        sk = keySchedule(sk, i)
    state = addRoundKey(state, sk)
    return state
