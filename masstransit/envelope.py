class Envelope(object):
    """
    This is the serialization wrapper class
    """
    
    def __init__(self, message_name, body):
        self.message_name = message_name
        self.body = body