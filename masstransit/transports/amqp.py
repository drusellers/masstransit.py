from amqplib import client_0_8 as amqp
import socket, logging, uuid
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
            msg = "Couldn't open a connection to %s:%s - %s" % (host, port, e)
            logging.fatal(msg)
            raise TransportOpenException(msg)
    
    def close(self):
        self.channel.close()
    
    def queue_declare(self, queue, durable, exclusive, auto_delete):
        logging.debug("declaring queue '%s'", queue)
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
    
    def bind(self, queue, kind, durable, auto_delete):
        logging.debug("declaring exchange '%s'", kind)
        self.channel.exchange_declare(
            exchange=kind,
            durable=durable,
            type='fanout',
            auto_delete=auto_delete
        )
        
        logging.debug("binding '%s' directly to '%s'", queue, kind)
        self.channel.queue_bind(
            queue=queue,
            exchange=kind
        )
    
    def unbind(self, kind, queue):
        logging.debug("unbinding")
        self.channel.queue_unbind(
            queue=queue,
            exchange=kind
        )
    
    
    def monitor(self, queue, callback):
        self.channel.basic_consume(
            queue=queue,
            no_ack=True,
            callback=callback,
            consumer_tag=str(uuid.uuid4())
        )
       
        while True:
            gevent.spawn(self._wait).join()
    
    def basic_publish(self, envelope, exchange):
        logging.debug('publishing to %s', exchange)
        message = self.create_message(envelope)
        self.channel.basic_publish(
            message,
            exchange = exchange
        )
    
    def _wait(self):
        self.channel.wait()