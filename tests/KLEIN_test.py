import unittest
import blockciphers.KLEIN as KLEIN

class KLEINTest(unittest.TestCase):

    def setUp(self):
        self.klein64 = KLEIN.KLEIN(nr=12, size=64)
        self.klein80 = KLEIN.KLEIN(nr=16, size=80)
        self.klein96 = KLEIN.KLEIN(nr=20, size=96)

    def test_sbox_nibble(self):
        self.assertEqual(KLEIN.sbox_nibble(0x01234567, 3, 32),
                         0x01294567)
        self.assertEqual(KLEIN.sbox_nibble(0x0123456789ABCDEF, 12, 64),
                         0x123456789AB8DEF)

    def test_addRoundKey(self):
        self.assertEqual(self.klein64.addRoundKey(0x0123456789ABCDEF,
                                                  0xFFFFFFFFFFFFFFFF),
                         0xFEDCBA9876543210)

    def test_subNibbles(self):
        self.assertEqual(self.klein64.subNibbles(0x0123456789ABCDEF),
                         0x74A91FB0C3268ED5)

    def test_rotateNibbles(self):
        self.assertEqual(self.klein64.rotateNibbles(0x0123456789ABCDEF),
                         0x456789ABCDEF0123)

    def test_mixNibbles(self):
        self.assertEqual(self.klein64.mixNibbles(0x23C0B5F19A47DE86),
                         0x598d9ae9beebeb3b)

    def test_keySchedule(self):
        self.assertEqual(self.klein64.keySchedule(0x1234567890ABCDEF, 1),
                         0xABCDEE909F363082)

    def test_testvectors64(self):
        def v(key, plaintext, ciphertext):
            self.assertEqual(self.klein64.encrypt(plaintext, key), ciphertext)
        v(0xFFFFFFFFFFFFFFFF, 0x0000000000000000, 0x6456764E8602E154)
        v(0xFFFFFFFFFFFFFFFF, 0x0000000000000000, 0x6456764E8602E154)
        v(0x1234567890ABCDEF, 0xFFFFFFFFFFFFFFFF, 0x592356C4997176C8)
        v(0x0000000000000000, 0x1234567890ABCDEF, 0x629F9D6DFF95800E)

    def test_testvectors80(self):
        def v(key, plaintext, ciphertext):
            self.assertEqual(self.klein80.encrypt(plaintext, key), ciphertext)
        v(0x00000000000000000000, 0xFFFFFFFFFFFFFFFF, 0x6677E20D1A53A431)
        v(0xFFFFFFFFFFFFFFFFFFFF, 0x0000000000000000, 0x82247502273DCC5F)
        v(0x1234567890ABCDEF1234, 0xFFFFFFFFFFFFFFFF, 0x3F210F67CB23687A)
        v(0x00000000000000000000, 0x1234567890ABCDEF, 0xBA5239E93E784366)

    def test_testvectors96(self):
        def v(key, plaintext, ciphertext):
            self.assertEqual(self.klein96.encrypt(plaintext, key), ciphertext)
        v(0x000000000000000000000000, 0xFFFFFFFFFFFFFFFF, 0xDB9FA7D33D8E8E36)
        v(0xFFFFFFFFFFFFFFFFFFFFFFFF, 0x0000000000000000, 0x15A3A03386A7FEC6)
        v(0x1234567890ABCDEF12345678, 0xFFFFFFFFFFFFFFFF, 0x79687798AFDA0BC3)
        v(0x000000000000000000000000, 0x1234567890ABCDEF, 0x5006A987A500BFDD)
        
if __name__ == '__main__':
    unittest.main()
