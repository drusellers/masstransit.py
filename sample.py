from masstransit.bus import Bus
from masstransit.config import Config

#@message('')
class MyMessage(object):
    def __init__(self):
        self.name = 'lawrence'

def dostuff(msg):
    print msg.name

class Consumer(object):
    def __call__(self, msg):
        print "consumer: '%s'" % (msg.name)

#this needs to be a bit fancier
b = Bus(Config())

b.subscribe('MyMessage', dostuff)
b.subscribe('MyMessage', Consumer())

b.subscribe(MyMessage, dostuff)

#b.Subscribe<MyMessage>(msg=>Console.WriteLine(msg.Name));

msg = MyMessage()

b.publish(msg)
#print

b.consume()