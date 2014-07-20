#! /usr/bin/env python

# the main motivation for not using the abc module here is to maintain
# compatibility with Python 2. This might be refactored in the future.


def get_bit(val, i):
    return int(val & (1 << i) != 0)


class QUARK_ABC(object):

    @property
    def c(self):
        raise NotImplementedError("Capacity c not specified")

    @property
    def r(self):
        raise NotImplementedError("Rate r not specified")

    @property
    def n(self):
        raise NotImplementedError("Output length n not specified")

    def f(self, X):
        raise NotImplementedError("Function f not implemented!")

    def g(self, Y):
        raise NotImplementedError("Function g not implemented!")

    def h(self, X, Y, L):
        raise NotImplementedError("Function h not implemented!")

    def initialise(self, m, prefix_zeros=0):
        m = m << 1 | 1
        l = len(bin(m)) - 2 + prefix_zeros  # -2 for 0b prefix
        return m << (self.r - l % self.r)
    
    def absorb(self, m):
        pass

    def squeeze(self, s):
        pass        

    def hash(self, m, prefix_zeros=0):
        m = initialise(m, prefix_zeros)
        s = absorb(m)
        return squeeze(s)
        
class U_QUARK(QUARK_ABC):

    r = 8
    c = 128
    n = 136


class D_QUARK(QUARK_ABC):

    r = 16
    c = 160
    n = 176


class S_QUARK(QUARK_ABC):

    r = 32
    c = 224
    n = 256
