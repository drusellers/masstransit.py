import json
from message import Message

class Serializer(object):
    
    def serialize(self, obj):
        data = self.todict(obj)
        #need to check all of the keys
        return json.dumps(data)
    
    def deserialize(self, data):
        dic = json.loads(data)
        msg = Message(dic)
        return msg
    
    def todict(self, obj):
        data = {}
        for key, value in obj.__dict__.iteritems():
            try:
                data[key] = self.todict(value)
            except AttributeError:
                data[key] = value
        return data
    
