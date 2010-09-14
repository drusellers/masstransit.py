from serializer import Serializer
from transports.amqp import AMQP

class Config(object):
    """
    This object holds all the settings for getting a bus up and running
    and contains sensible defaults as well.
    """
    def __init__(self):
        self.transport = AMQP()
        self.serializer = Serializer() #default json serializer
        self.host = '172.16.43.141'
        self.user_id = 'guest'
        self.password = 'guest'
        self.vhost = '/'
        self.port = 5672
        self.insist = False
        self.queue = 'default_queue'
        self.routing_key = 'default_routing_key'
        self.exchange = 'default_exchange'
        self.durable = True
        self.exclusive = False
        self.auto_delete = False
        self.deliver_mode = 2 #what is this?
