import uuid, logging
from message import Message

class Bus(object):
    """
    publish and subscribe are the key methods on this class
    """
    def dispatch(self, message):
        decoded = self.serializer.deserialize(message.body)
        msg_name = decoded['kind']
        msg_data = decoded['data']
        logging.debug("consuming message '%s'" % (msg_name)) 
        callback = self.subscriptions[msg_name]
        if callback:
            callback(Message(msg_data))

    def __init__(self, config):
        self.subscriptions = {}
        self.serializer = config.serializer
        self.connection = config.transport.create_connection('172.16.43.141','guest','guest','/','5672')
        self.channel = self.connection.connection.channel()
        self.transport = config.transport
        self._queue(config)
        self.durable = config.durable #ugly: _bind
        self.auto_delete = config.auto_delete #ugly: _bind
        self.channel.basic_consume( #is this continual
            queue = self.queue,
            no_ack = True,
            callback = self.dispatch,
            consumer_tag = str(uuid.uuid4())
        )

    def publish(self, message):
        """
        this will publish the message object to an exchange in rabbitmq that
        is equal to the message class name. this is a direct concept from
        .net and should be adopted to a more pythonic manner
        """
        msg_name = message.__class__.__name__
        msg_data = message
        envelope = self.serializer.serialize({'kind':msg_name,'data':msg_data})
        message = self.transport.create_message(envelope)
        logging.debug('publishing %s', msg_name)
        self.channel.basic_publish(
            message,
            exchange = msg_name)
        
    def subscribe(self, kind, callback):
        """
        this will register an exchange in rabbitmq for the 'kind' and then bind
        the queue to that exchange. it then sets the subscriptions[kind] to the
        callback provided.
        """
        if type(kind) == type:
            kind = kind.__name__
        
        self._bind(kind)
        self.subscriptions[kind]=callback

    def unsubscribe(self, kind):
        if type(kind) == type:
            kind = kind.__name__
        
        self._unbind(kind)
        del self.subscriptions[kind]

    def close(self):
        logging.debug("closing the bus at '%s'", self.queue)
        #move to transport? what is the abstraction here?
        if getattr(self,'channel'):
            self.channel.close()
        
        #move to transport - i only need one connection
        if getattr(self, 'connection'):
            self.connection.close()

    def _bind(self, kind):
        logging.debug("declaring exchange '%s'", kind)
        self.channel.exchange_declare(
            exchange = kind,
            type = 'direct',
            durable = self.durable,
            auto_delete = self.auto_delete
        )

        logging.debug("binding '%s' directly to '%s'", self.queue, kind)
        self.channel.queue_bind(
            queue = self.queue,
            exchange = kind
        )

    def _queue(self, config):
        self.queue = config.queue
        logging.debug("declaring queue '%s'", self.queue)
        self.channel.queue_declare(
            queue = config.queue,
            durable = config.durable,
            exclusive = config.exclusive,
            auto_delete = config.auto_delete
        )

    def _unbind(self, kind):
        #have no idea how to do this
        logging.debug("unbinding '%s' from '%s'", self.queue, kind)

    def _dequeue(self, queue):
        #have no idea how to do this, do I care?
        logging.debug("undeclaring queue '%s'", queue)
