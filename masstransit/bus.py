from gevent.monkey import patch_all
patch_all()

import uuid, logging
from message import Message
from masstransit import counters
import gevent

class Bus(object):
    """
    publish and subscribe are the key methods on this class
    """
    
    def __init__(self, config):
        self.subscriptions = {}
        self.serializer = config.serializer
        self.transport = config.transport
        self.transport.open(config.host, vhost=config.vhost)
        self._queue(config)
        self.durable = config.durable #ugly: _bind
        self.auto_delete = config.auto_delete #ugly: _bind
    
    def publish(self, message):
        """
        this will publish the message object to an exchange in rabbitmq that
        is equal to the message class name. this is a direct concept from
        .net and should be adopted to a more pythonic manner
        """
        msg_name = message.__class__.__name__
        msg_data = message
        envelope = self.serializer.serialize({'kind':msg_name, 'data':msg_data})
        message = self.transport.create_message(envelope)
        logging.debug('publishing %s', msg_name)
        self.transport.basic_publish(message, exchange=msg_name)
    
    def subscribe(self, kind, callback):
        """
        this will register an exchange in rabbitmq for the 'kind' and then bind
        the queue to that exchange. it then sets the subscriptions[kind] to the
        callback provided.
        """
        if type(kind) == type:
            kind = kind.__name__
        
        self._bind(kind)
        if not kind in self.subscriptions:
            self.subscriptions[kind]=[]
        self.subscriptions[kind].append(callback)
    
    def dispatch(self, message):
        decoded = self.serializer.deserialize(message.body)
        msg_name = decoded['kind']
        msg_data = decoded['data']
        counters.increment(msg_name)
        logging.debug("consuming message '%s'" % (msg_name)) 
        callbacks = self.subscriptions[msg_name]
        for callback in callbacks:
            callback(Message(msg_data))
    
    def start(self):
        """
        Tells the bus to start listening for messages. This method blocks
        forever. Need to come up with a better paradigm.
        """
        self.transport.basic_consume(
            queue=self.queue,
            no_ack=True,
            callback=self.dispatch,
            consumer_tag=str(uuid.uuid4())
        )
        
        self.generate_statistics()
        self.transport.monitor()

    def generate_statistics(self):
        stats = counters.raw_stats()
        msg = counters.StatisticsUpdate(stats)
        print stats
        self.publish(msg)
        gevent.spawn_later(1, self.generate_statistics)
    
    def get(self):
        return self.transport.basic_get(self.queue)
    
    def unsubscribe(self, kind):
        if type(kind) == type:
            kind = kind.__name__
        self._unbind(kind)
        del self.subscriptions[kind]
    
    def close(self):
        logging.debug("closing the bus at '%s'", self.queue)
        if getattr(self, 'transport'):
            self.transport.close()

    def _bind(self, kind):
        logging.debug("declaring exchange '%s'", kind)
        self.transport.exchange_declare(
            exchange=kind,
            durable=self.durable,
            auto_delete=self.auto_delete
        )

        logging.debug("binding '%s' directly to '%s'", self.queue, kind)
        self.transport.queue_bind(
            queue=self.queue,
            exchange=kind
        )

    def _queue(self, config):
        self.queue = config.queue
        logging.debug("declaring queue '%s'", self.queue)
        self.transport.queue_declare(
            queue=config.queue,
            durable=config.durable,
            exclusive=config.exclusive,
            auto_delete=config.auto_delete
        )

    def _unbind(self, kind):
        logging.debug("unbinding '%s' from '%s'", self.queue, kind)

    def _dequeue(self, queue):
        logging.debug("undeclaring queue '%s'", queue)
        self.transpor.queue_delete(
            queue=self.queue
        )
