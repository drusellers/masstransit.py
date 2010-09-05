import unittest
from masstransit.message import Message

class MessageTests(unittest.TestCase):
    def test_simple_dict(self):
        d = {'name': 'dru'}
        m = Message(d)
        self.assertEqual('dru', m.name)

    def test_depth_of_one(self):
        d = {'name': 'dru', 'address': { 'street': '236' }}
        m = Message(d)
        self.assertEqual('dru', m.name)
        self.assertEqual('236', m.address.street)
