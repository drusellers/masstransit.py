from amqplib import client_0_8 as amqp

class AMQP:
    def create_message(self, data):
        return amqp.Message(data)

#default port is 5672
    def create_connection(self, host, user_id, password, vhost, port):
        connection = amqp.Connection(
            host = '%s:%s' % (host, port),
            user_id=user_id,
            password = password,
            virtual_host = vhost,
            insist = True
        )
        return connection
