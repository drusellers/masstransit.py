from amqplib import client_0_8 as amqp

class AMQP(object):
    """
    This transport is used when talking to AMQP/RabbitMQ
    """

    def create_message(self, data):
        """
        creates a message class for the AMQP transport
        """
        return amqp.Message(data)

    def create_connection(self, host, user_id, password, vhost, port):
        """
        creates a connection to the AMQP server
        default port is 5672
        """
        connection = amqp.Connection(
            host = '%s:%s' % (host, port),
            user_id=user_id,
            password = password,
            virtual_host = vhost,
            insist = True
        )
        return connection
