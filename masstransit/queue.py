class Queue:
    def __init__(self, channel, address, durable, exclusive, auto_delete):
		self.queue = address
        channel.queue_declare(
            queue = self.queue,
            durable = durable,
            exclusive = exclusive,
            auto_delete = auto_delete
        )
