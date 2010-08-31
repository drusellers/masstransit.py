class Connection(object):
    def __init__(self, host=DEFAULT_HOST, user_id=DEFAULT_USER_ID,
        password=DEFAULT_PASSWORD, vhost=DEFAULT_VHOST, port=DEFAULT_PORT,
        insist=DEFAULT_INSIST):

        self.host = host
        self.user_id = user_id
        self.password = password
        self.vhost = vhost
        self.port = port
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
