from gevent.monkey import patch_all
import gevent
patch_all()

import logging
from message import Message
from masstransit import counters
from collections import defaultdict

#durability a bus level or transport level choice?
#temp subscription = auto-delete: true
#perm subscription = auto-delete: false
class Bus(object):
    """
    The bus abstracts the desired transportation, and manages the callbacks
    """
    
    def __init__(self, config):
        self.subscriptions = defaultdict(list)
        self.serializer = config.serializer
        self.transport = config.transport
        self.queue = config.queue
        self.durable = config.durable #ugly: bind
        self.auto_delete = config.auto_delete #ugly: bind
        self.transport.open(config.host, vhost=config.vhost)
        self.transport.queue_declare(
            queue=config.queue,
            durable=config.durable,
            exclusive=config.exclusive,
            auto_delete=config.auto_delete
        )
    
    def publish(self, message):
        """
        this will publish the message object to an exchange in rabbitmq that
        is equal to the message class name. this is a direct concept from
        .net and should be adopted to a more pythonic manner
        """
        msg_name = message.__class__.__name__
        msg_data = message
        envelope = self.serializer.serialize({'kind':msg_name, 'data':msg_data})
        self.transport.basic_publish(envelope, exchange=msg_name)
    
    #persistant | transient?
    def subscribe(self, kind, callback):
        """
        this will register an exchange in rabbitmq for the 'kind' and then bind
        the queue to that exchange. it then sets the subscriptions[kind] to the
        callback provided.
        """
        if type(kind) == type:
            kind = kind.__name__
        
        self.transport.bind(self.queue, kind, self.durable, self.auto_delete)
        self.subscriptions[kind].append(callback)
    
    def unsubscribe(self, kind):
        """
        this will unregister the queue with the exchange in rabbitmq for the
        'kind'. It then removes the callbacks in the subscriptions[kind]
        """
        if type(kind) == type:
            kind = kind.__name__
        
        self.transport.unbind(kind, self.queue)
        if kind in self.subscriptions:
            del self.subscriptions[kind]
    
    def start(self):
        """
        Tells the bus to start listening for messages. This method blocks
        forever. Need to implement a better ctrl-c support.
        """
        self._generate_statistics()
        self.transport.monitor(self.queue, self._dispatch)
    
    def close(self):
        logging.debug("closing the bus at '%s'", self.queue)
        if getattr(self, 'transport'):
            self.transport.close()
    
    def _dispatch(self, message):
        envelope = self.serializer.deserialize(message.body)
        msg_name = envelope['kind']
        msg_data = envelope['data']
#        counters.increment(msg_name)
        logging.debug("consuming message '%s'", msg_name) 
        for callback in self.subscriptions[msg_name]:
            callback(Message(msg_data))
    
    def _generate_statistics(self):
        stats = counters.raw_stats()
        msg = counters.StatisticsUpdate(stats)
        self.publish(msg)
        gevent.spawn_later(1, self._generate_statistics)
