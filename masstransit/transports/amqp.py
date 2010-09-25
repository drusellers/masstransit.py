from amqplib import client_0_8 as amqp
import socket
import logging
from masstransit.exceptions import TransportOpenException
import gevent

class AMQP(object):
    """
    This transport is used when talking to AMQP/RabbitMQ
    """

    def open(self, host, vhost, user_id = 'guest', password = 'guest', port = 5672):
        """
        creates a connection to the AMQP server
        default port is 5672
        Will throw a TransportOpenException if it can't open the AMQP connection
        """
        try:
            self.connection = amqp.Connection(
                host = '%s:%s' % (host, port),
                user_id = user_id,
                password = password,
                virtual_host = vhost,
                insist = True
            )
            self.channel = self.connection.channel()
        except socket.error, e:
            msg = "Couldn't open a connection to %s:%s" % (host, port)
            logging.fatal(msg)
            raise TransportOpenException(msg)
    
    def exchange_declare(self, exchange, durable, auto_delete):
        self.channel.exchange_declare(
            exchange = exchange,
            type = 'direct',
            durable = durable,
            auto_delete = auto_delete
        )
    
    def queue_bind(self, queue, exchange):
        self.channel.queue_bind(
            queue = queue,
            exchange = exchange
        )
    
    def queue_declare(self, queue, durable, exclusive, auto_delete):
        self.channel.queue_declare(
            queue = queue,
            durable = durable,
            exclusive = exclusive,
            auto_delete = auto_delete
        )
    
    def queue_delete(self, queue):
        self.channel.queue_delete(
            queue = queue
        )
    
    def create_message(self, data):
        """
        creates a message class for the AMQP transport
        """
        return amqp.Message(data)
    
    def close(self):
        self.channel.close()
    
    def basic_get(self, queue, no_ack=True):
        return self.channel.basic_get(
                    queue,
                    no_ack=no_ack)
    
    def basic_consume(self, queue, no_ack, callback, consumer_tag):
        self.channel.basic_consume( #is this continual
            queue = queue,
            no_ack = no_ack,
            callback = callback,
            consumer_tag = consumer_tag
        )
    
    def monitor(self):
        while True:
            gevent.spawn(self.wait).join()
    
    def wait(self):
        self.channel.wait()
    
    def basic_publish(self, message, exchange):
        self.channel.basic_publish(
            message,
            exchange = exchange
        )