from masstransit.bus import Bus
from masstransit.config import Config

cfg = Config()
bus = Bus(cfg)

class MyMessage:
    def __init__(self, content):
        self.content = content

def handle(msg):
    print msg.content

msg = MyMessage('lawrence')
bus.subscribe(msg.__class__.__name__, handle)
bus.publish(msg)
