import uuid
from amqplib import client_0_8 as amqp

class Bus:
    def __init__(self, config):
        subscriptions = {}
        self.serializer = Serializer()
        self.connection = Connection('172.16.43.141','guest','guest','/','5672',True)
		self.channel = self.connection.channel()

		self.queue = config.queue
		self.durable = config.durable
		self.exclusive = config.excusive
		self.auto_delete = config.auto_delete
        self.channel.queue_declare(
            queue=self.queue,
            durable=self.durable,
            exclusive=self.exclusive,
            auto_delete=self.auto_delete
        )

        self.channel.basic_consume(
            queue=self.queue,
            no_ack=True,
            callback=self.dispatch,
            consumer_tag=str(uuid.uuid4())
        )
	    
    def publish(self, message):
        msg_name = message.__class__.__name__
        msg_data = message
        envelope = self.serializer.serialize({'kind':msg_name,'data':msg_data})
        #how to do this better
    	message = Message.create(envelope)
    	self.channel.basic_publish(
            message,
            exchange = msg_name) 

    def subscribe(self, kind, callback):
        self._bind(kind)
		self.subscriptions[kind]=callback
	
	def unsubscribe(self, kind):
        self._unbind(kind)
		del self.subscriptions[kind]

    def dispatch(self, message):
        decoded = self.serializer.deserialize(message.body)
        msg_name = decoded['kind']
        msg_data = decoded['data']
        callback = self.subscriptions[msg_name]
        if callback:
            callback(Message(msg_data))

    def close(self):
        if getattr(self,'channel'):
            self.channel.close()
        if getattr(self, 'connection'):
            self.connection.close()

    def _bind(self, kind):
        self.channel.exchange_declare(
            exchange = kind,
            type = 'direct',
            durable = self.durable,
            auto_delete = self.auto_delete
        )

        self.channel.queue_bind(
            queue=self.queue,
            exchange=kind
        )

    def _unbind(self, kind):
        pass #have no idea how to do this yet
