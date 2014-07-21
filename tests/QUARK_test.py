import unittest
import hashfunctions.QUARK as QUARK


class QUARKTest(unittest.TestCase):

    def setUp(self):
        self.U = QUARK.U_QUARK()
        self.D = QUARK.D_QUARK()
        self.S = QUARK.S_QUARK()

    def test_initialise(self):
        self.assertEqual(0x80, self.U.initialise(0, 0)[0])
        self.assertEqual(0x8000, self.D.initialise(0, 0)[0])
        self.assertEqual(0x80000000, self.S.initialise(0, 0)[0])

    def test_IV(self):
        self.assertEqual(0xD8DACA44414A099719C80AA3AF0656445B,
                         0x80 ^ self.U.IV)
        self.assertEqual(0xCC6C4AB7D11FA9BDF6EEDE03D87B68F91BAA706CA0E9,
                         0x8000 ^ self.D.IV)
        self.assertEqual(0x397251CEE1DE8AA73EA26250C6D7BE128CD3E79DD718C24B8A19D09CA492DA5D,
                         0x80000000 ^ self.S.IV)

    def test_absorb(self):
        self.assertEqual(0x9A03A9DEFBB9ED3867DAB18EC039276212,
                         self.U.absorb(0x80, 1))
        self.assertEqual(0xE1AFDDED75F72D33AE3F60D3A1A9E9FA759AC6F082C7,
                         self.D.absorb(0x8000, 1))
        self.assertEqual(0x3D63F54100A7BC5135692F3BDE1563F7998A6965FE6D26AB40262D2003256214,
                         self.S.absorb(0x80000000, 1))

    def test_hash(self):
        self.assertEqual(0x126B75BCAB23144750D08BA313BBD800A4,
                         self.U.hash(0))
        self.assertEqual(0x82C7F380E231578E2FF4C2A402E18BF37AEA8477298D,
                         self.D.hash(0))
        self.assertEqual(0x03256214B92E811C321AE86BAB4B0E7AE9C22C42882FCCDE8C22BFF6A0A1D6F1,
                         self.S.hash(0))

if __name__ == '__main__':
    unittest.main()
