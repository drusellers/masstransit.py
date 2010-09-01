class Message(object):
    def __init__(self,json_data):
        self.json_data = json_data

    def __getattr__(self, name):
        if (self.json_data.has_key(name)):
            #how to handle nested hierarchies
            return self.json_data[name]
        else:
           raise AttributeError,name

