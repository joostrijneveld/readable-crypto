import unittest
import blockciphers.PRESENT as PRESENT


class PRESENTTest(unittest.TestCase):

    def setUp(self):
        self.present80 = PRESENT.PRESENT(size=80)

    def test_sBoxlayer(self):
        self.assertEqual(self.present80.sBoxlayer(0x0123456789ABCDEF),
                         0xC56B90AD3EF84712)
    
    def test_pLayer(self):
        self.assertEqual(self.present80.pLayer(0x0123456789ABCDEF),
                         0x00FF0F0F33335555)
    
    def test_keySchedule(self):
        self.assertEqual(self.present80.keySchedule(0xF0F0F0F0F0F0F0F0F0F0, 1),
                         0x5E1E1E1E1E1E1E1E9E1E)
        
    def test_testvectors80(self):
        def v(plaintext, key, ciphertext):
            self.assertEqual(self.present80.encrypt(plaintext, key), ciphertext)
        v(0x0000000000000000, 0x00000000000000000000, 0x5579C1387B228445)
        v(0x0000000000000000, 0xFFFFFFFFFFFFFFFFFFFF, 0xE72C46C0F5945049)
        v(0xFFFFFFFFFFFFFFFF, 0x00000000000000000000, 0xA112FFC72F68417B)
        v(0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFFFFFF, 0x3333DCD3213210D2)
    
if __name__ == '__main__':
    unittest.main()
