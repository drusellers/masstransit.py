from masstransit.config import Config
from masstransit.bus import Bus
import unittest
from nose.plugins.attrib import attr

class BusMessage:
    def __init__(self):
        self.greeting = 'hi'

class BusTest(unittest.TestCase):
    @attr('integration')
    def test_start(self):
        cfg = Config()
        bus = Bus(cfg)
        msg = BusMessage()
        bus.publish(msg)
