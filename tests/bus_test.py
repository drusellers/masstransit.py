from masstransit.config import Config
from masstransit.bus import Bus
import unittest
from nose.plugins.attrib import attr
import fudge

class BusMessage(object):
    def __init__(self):
        self.greeting = 'hi'

class BusTest(unittest.TestCase):
    
    def setUp(self):
        cfg = Config()
        t = (fudge.Fake('tranny')
                .provides('open')
                .provides('basic_publish')
                .provides('unbind')
                .provides('bind')
                .provides('queue_declare'))
        cfg.transport = t
        self.cfg = cfg
    
    def test_start(self):
        bus = Bus(self.cfg)
        msg = BusMessage()
        bus.publish(msg)
    
    def test_blank_unsubscribe(self):
        bus = Bus(self.cfg)
        bus.unsubscribe(BusMessage)
    
    def test_unsubscribe(self):
        bus = Bus(self.cfg)
        bus.subscribe('test', lambda x: 1)
        bus.unsubscribe('test')
    
    def test_subscribe_type(self):
        bus = Bus(self.cfg)
        bus.subscribe(BusMessage, lambda x: 1)

    #test_start
    """
    def test_dispatch(self):
        bus = Bus(self.cfg)
        self.a = False
        def doit(msg):
            self.a = True
        
        msg = fudge.Fake('msg').has_attr(
            body = '{"kind": "test", "data": "{}"}'
            )
        
        bus.subscribe('test', doit)
        bus._dispatch(msg)
        self.assertEqual(True, self.a)
    """
    def tearDown(self):
        fudge.verify()