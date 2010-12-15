from masstransit.config import config_file
import unittest
import ConfigParser, os

class ConfigTests(unittest.TestCase):
    
    def setUp(self):
        self.config = config_file('./tests/test.cfg')
        
    def test_queue(self):
        self.assertEqual('qest', self.config.queue)
    
    def test_host(self):
        self.assertEqual('localhost', self.config.host)
    
    def test_port(self):
        self.assertEqual(2231, self.config.port)
    
    def test_vhost(self):
        self.assertEqual('/a', self.config.vhost)
    
    def test_user_id(self):
        self.assertEqual('guest', self.config.user_id)
    
    def test_password(self):
        self.assertEqual('guest', self.config.password)