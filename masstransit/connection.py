from amqplib import client_0_8 as amqp

class Connection(object):
    def __init__(self, host, user_id, password, vhost, port, insist):
        self.host = host #ip address or localhost
        self.user_id = user_id 
        self.password = password
        self.vhost = vhost 
        self.port = port #5672
        self.insist = insist

        self.connect()

    def connect(self):
        self.connection = amqp.Connection(
            host='%s:%s' % (self.host, self.port),
            userid=self.user_id,
            password=self.password,
            virtual_host=self.vhost,
            insist=self.insist
        )

    def channel(self):
        self.channel = self.connection.connection.channel()
        return self.channel
