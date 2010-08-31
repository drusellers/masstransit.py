class Consumer(object):
    def __init__(self, routing_key=DEFAULT_ROUTING_KEY,
        exchange=DEFAULT_EXCHANGE, queue=DEFAULT_QUEUE,
        durable=DEFAULT_DURABLE, exclusive=DEFAULT_EXCLUSIVE,
        auto_delete=DEFAULT_AUTO_DELETE, connection=None):

        self.callbacks = {}

        self.routing_key = routing_key
        self.exchange = exchange
        self.queue = queue
        self.durable = durable
        self.exclusive = exclusive
        self.auto_delete = auto_delete
        self.connection = connection or Connection()
        self.channel = self.connection.connection.channel()

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

    def close(self):
        if getattr(self, 'channel'):
            self.channel.close()
        if getattr(self, 'connection'):
            self.connection.close()

    def wait(self):
        while True:
            self.channel.wait()

    def dispatch(self, message):
        decoded = simplejson.loads(message.body)
        message.body = decoded['data']
        callback = self.callbacks.get(decoded['kind'])
        if callback:
            callback(message)

    def register(self, kind, callback):
        self.callbacks[kind] = callback

    def unregister(self, kind):
        del self.callbacks[kind]

