import json
import uuid
from amqplib import client_0_8 as amqp

class BusConfiguration:
	def __init__(self):
		self.host = '127.0.0.1'
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

class Bus:
    def __init__(self, options):
		self.durable =o ptions.durable
		self.auto_delete = option.auto_delete
		self.connection = #hmm
		self.channel = self.connection.connection.channel()
		self.exchange = options.exchange
		self.queue = options.queue
		self.routing_key = options.routing_key
		self.delivery_mode = options.delivery_mode
		self.subscriptions = {}
		self.exclusive = options.excusive
		
        self.channel.queue_declare(
            queue=self.queue,
            durable=self.durable,
            exclusive=self.exclusive,
            auto_delete=self.auto_delete
        )
        self.channel.exchange_declare(
            exchange=self.exchange,
            type='direct',
            durable=self.durable,
            auto_delete=self.auto_delete
        )
        self.channel.queue_bind(
            queue=self.queue,
            exchange=self.exchange,
            routing_key=self.routing_key
        )
        self.channel.basic_consume(
            queue=self.queue,
            no_ack=True,
            callback=self.dispatch,
            consumer_tag=str(uuid.uuid4())
        )
	    
    def publish(self, message):
        json_name = message.__class__.__name__
		json_data = json.dumps(message.__dict__)
		envelope = json.dumps({'kind':json_name,'data':json_data})
		message = amqp.Message(envelope)
		self.channel.basic_publish(#lean this
			message,
			exchange = self.exchange, #learn exchange
			routing_key = self.routing_key) #learn routing key

    def subscribe(self, kind, callback):
		self.subscriptions[kind]=callback
	
	def unsubscribe(self, kind):
		del self.callbacks[kind]


    def close(self):
        if getattr(self,'channel'):
            self.channel.close()
        if getattr(self, 'connection'):
            self.connection.close()

