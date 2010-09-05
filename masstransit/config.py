class Config:
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
