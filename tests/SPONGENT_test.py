import unittest
import hashfunctions.SPONGENT as SPONGENT


class SPONGENTTest(unittest.TestCase):

    def setUp(self):
        self.spongent80 = SPONGENT.SPONGENT(n=88, c=80, r=8, R=45)

    def test_sBoxLayer(self):
        self.assertEqual(self.spongent80.sBoxLayer(0x0123456789ABCDEF012345),
                         0xEDB0214F7A859C36EDB021)

    def test_pLayer(self):
        self.assertEqual(self.spongent80.pLayer(0x0123456789ABCDEF012345),
                         0x00FF003C3C333333155555)

    def test_lCounter(self):
        lfsr = [0x0a, 0x14, 0x29, 0x13, 0x27, 0x0f, 0x1e, 0x3d, 0x3a, 0x34,
                0x28, 0x11, 0x23, 0x07, 0x0e, 0x1c, 0x39, 0x32, 0x24, 0x09,
                0x12, 0x25, 0x0b, 0x16, 0x2d, 0x1b, 0x37, 0x2e, 0x1d, 0x3b,
                0x36, 0x2c, 0x19, 0x33, 0x26, 0x0d, 0x1a, 0x35, 0x2a, 0x15,
                0x2b, 0x17, 0x2f, 0x1f, 0x3f]
        for x in lfsr:
            self.spongent80.lCounter()
            self.assertEqual(self.spongent80.LFSR, x)
    
    def test_P(self):
        self.assertEqual(self.spongent80.P(0x0000000000000000000053),
                         0xF69A7BE47D03C39920CD9E)
          
    def test_hash(self):
        m = 0x53706F6E6765202B2050726573656E74203D2053706F6E67656E74
        self.assertEqual(0x69971BF96DEF95BFC46822,
                         self.spongent80.hash(m, prefix_zeros=1))

if __name__ == '__main__':
    unittest.main()


