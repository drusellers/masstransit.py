class Publisher(object):
    def __init__(self, routing_key=DEFAULT_ROUTING_KEY,
        exchange=DEFAULT_EXCHANGE, connection=None,
        delivery_mode=DEFAULT_DELIVERY_MODE):

        self.connection = connection or Connection()
        self.channel = self.connection.connection.channel()
        self.exchange = exchange
        self.routing_key = routing_key
        self.delivery_mode = delivery_mode

    def publish(self, kind, message_data):
        encoded = simplejson.dumps({'kind': kind, 'data': message_data})
        message = amqp.Message(encoded)
        message.properties['delivery_mode'] = self.delivery_mode
        self.channel.basic_publish(
            message,
            exchange=self.exchange,
            routing_key=self.routing_key
        )
        return message

    def close(self):
        if getattr(self, 'channel'):
            self.channel.close()
        if getattr(self, 'connection'):
            self.connection.connection.close()

