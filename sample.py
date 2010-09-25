from masstransit.bus import Bus
from masstransit.config import config_file
import time
import logging

LOG_FILENAME = 'test.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


class MyMessage(object):
    def __init__(self):
        self.name = 'lawrence'


def dostuff(msg):
    logging.info("dostuff: %s", msg.name)


class Consumer(object):
    def __call__(self, msg):
        logging.info("consumer callable: '%s'", msg.name)


b = Bus(config_file('sample.cfg'))

b.subscribe('MyMessage', dostuff)
#b.subscribe('MyMessage', Consumer())
#b.subscribe(MyMessage, dostuff)

msg = MyMessage()
#for i in xrange(1,10000):
#    b.publish(msg)
#b.publish(msg)

#start the message pulling
#import datetime
#print datetime.datetime.now()
b.start()

