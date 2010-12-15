import sys
sys.path.append('..')

from masstransit.bus import Bus
from masstransit.config import config_file
import time
import logging
from masstransit.counters import StatisticsUpdate

LOG_FILENAME = 'test_pub.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


class MyMessage(object):
    def __init__(self):
        self.name = 'lawrence'

b = Bus(config_file('sample_publisher.cfg'))

msg = MyMessage()
for i in xrange(1,20000):
    b.publish(msg)
