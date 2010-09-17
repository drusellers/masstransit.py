from masstransit.bus import Bus
from masstransit.config import config_file
import time
import logging

LOG_FILENAME = 'test.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

#@message('')
class MyMessage(object):
    def __init__(self):
        self.name = 'lawrence'

def dostuff(msg):
    logging.info(msg.name)

class Consumer(object):
    def __call__(self, msg):
        print "consumer: '%s'" % (msg.name)

#this needs to be a bit fancier
b = Bus(config_file('sample.cfg'))

b.subscribe('MyMessage', dostuff)
b.subscribe('MyMessage', Consumer())

b.subscribe(MyMessage, dostuff)

msg = MyMessage()

b.publish(msg)

print 'consuming'
b.consume()
time.sleep(3)