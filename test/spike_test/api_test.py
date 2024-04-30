import unittest

from pykiwoom.kiwoom import Kiwoom


class test(unittest.TestCase):

    def test_get_code(self):
        kiwoom = Kiwoom()
        kiwoom.CommConnect(block=True)

        kospi = kiwoom.GetCodeListByMarket("0")
        kosdaq = kiwoom.GetCodeListByMarket("10")
        etf = kiwoom.GetCodeListByMarket("8")

        print(len(kospi), kospi)
        print(len(kosdaq), kosdaq)
        print(len(etf), etf)
        self.assertEqual(1, 1)
