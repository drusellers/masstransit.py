import unittest

class BusMessage:
    def __init__(self):
        self.greeting = 'hi'

class BusTest(unittest.TestCase):
    def start(self):
        cfg = Config()
        bus = Bus(cfg)
        msg = BusMessage()
        bus.publish(msg)
