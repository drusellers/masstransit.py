from masstransit.config import config_file
import unittest
import ConfigParser, os

class ConfigTests(unittest.TestCase):
    def test_readingfiles(self):
        config = config_file('./tests/test.cfg')
        
        self.assertEqual('qest', config.queue)
        
        self.assertEqual('localhost', config.host)
        self.assertEqual(2231, config.port)
        self.assertEqual('/', config.vhost)
        self.assertEqual('guest', config.user_id)
        self.assertEqual('guest', config.password)