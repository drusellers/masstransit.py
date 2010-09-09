from masstransit.config import Config
from masstransit.bus import Bus
import unittest
from nose.plugins.attrib import attr

class BusMessage(object):
    def __init__(self):
        self.greeting = 'hi'

class MockChannel(object):
    def __init__(self):
        pass

class MockConnectionConnection(object):
    def __init__(self):
        self.channel = MockChannel()

    #def channel(self):
    #    return MockChannel()

class MockConnection(object):
    def __init__(self):
        self.connection = MockConnectionConnection()

class MockTransport(object):
    def create_message(self, data):
        return data

    def create_connection(self, host, user_id, password, vhost, port):
        return MockConnection()

class BusTest(unittest.TestCase):
    
    
    def setUp(self):
        cfg = Config()
        cfg.transport = MockTransport()
        self.cfg = cfg

    @attr('integration')
    def test_start(self):
        bus = Bus(self.cfg)
        msg = BusMessage()
        bus.publish(msg)
