import unittest
from masstransit.urn import Urn


class TestUrnSpecs(unittest.TestCase):
    class Msg(object):
        pass
    
    def test_class(self):
        urn = Urn(TestUrnSpecs.Msg)
        self.assertEqual('urn_test:Msg', urn.kind)
    
    def test_string(self):
        urn = Urn('TestUrnSpecs.Msg')
        self.assertEqual('TestUrnSpecs:Msg', urn.kind)