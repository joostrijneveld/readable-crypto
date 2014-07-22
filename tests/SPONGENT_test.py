import unittest
import hashfunctions.SPONGENT as SPONGENT


class SPONGENTTest(unittest.TestCase):

    def setUp(self):
        self.spongent80 = SPONGENT.SPONGENT(n=88, c=80, r=8, R=45)
        self.spongent128 = SPONGENT.SPONGENT(n=128, c=128, r=8, R=70)
        self.spongent160 = SPONGENT.SPONGENT(n=160, c=160, r=16, R=90)
        self.spongent224 = SPONGENT.SPONGENT(n=224, c=224, r=16, R=120)
        self.spongent256 = SPONGENT.SPONGENT(n=256, c=256, r=16, R=140)

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
        self.assertEqual(0x6B7BA35EB09DE0F8DEF06AE555694C53,
                         self.spongent128.hash(m, prefix_zeros=1))
        self.assertEqual(0x13188A4917EA29E258362C047B9BF00C22B5FE91,
                         self.spongent160.hash(m, prefix_zeros=1))
        self.assertEqual(0x8443B12D2EEE4E09969A183205F5F7F684A711A5BE079A15F4CCDC30,
                         self.spongent224.hash(m, prefix_zeros=1))
        self.assertEqual(0x67DC8FC8B2EDBA6E55F4E68EC4F2B2196FE38DF9B1A760F4D43B4669160BF5A8,
                         self.spongent256.hash(m, prefix_zeros=1))

if __name__ == '__main__':
    unittest.main()


