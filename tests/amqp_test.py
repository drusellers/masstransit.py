import unittest
from nose.plugins.attrib import attr
from masstransit.transports.amqp import AMQP

class AmqpTest(unittest.TestCase):
    
    def setUp(self):
        self.amqp = AMQP()
        self.amqp.open('localhost','/publisher')

    @attr('integration')
    def test_newingup(self):
        self.assertNotEqual(self.amqp, None)
        pass
    
    @attr('integration')
    def test_createmessage(self):
        msg = self.amqp.create_message('data')
    
    @attr('integration')
    def test_basicpublish(self):
        self.amqp.basic_publish('hello', 'unittest')
    
    @attr('integration')
    def test_bind(self):
        self.amqp.bind('dru', 'direct', True, True)
        
    @attr('integration')
    def test_unbind(self):
        self.amqp.unbind('direct','dru')
        
    def tearDown(self):
        self.amqp.close()

class AmqpOpenTest(unittest.TestCase):
    @attr('integration')
    def test_canopen(self):
        amqp = AMQP()
        amqp.open('localhost')
