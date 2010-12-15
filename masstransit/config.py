from serializer import Serializer
from transports.amqp import AMQP
import ConfigParser

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
        self.durable = True
        self.exclusive = False
        self.auto_delete = False
        self.deliver_mode = 2 #what is this?

def config_file(filepath):
    config = ConfigParser.ConfigParser()
    config.readfp(open(filepath))
    
    def s(key):
        return config.get('masstransit', key)
    def i(key):
        return config.getint('masstransit', key)
    
    cfg = Config()
    cfg.queue = s('queue')
    cfg.vhost = s('vhost')
    cfg.port = i('port')
    cfg.host = s('host')
    cfg.user_id = s('user_id')
    cfg.password = s('password')
    
    return cfg
