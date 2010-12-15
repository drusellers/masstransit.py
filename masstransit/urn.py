class Urn(object):
    def __init__(self, name):
        kind = name
        if type(kind) == type:
            kind = name.__module__ + "." + name.__name__
        
        urn = kind.replace('.',':')
        self.kind = urn
    
    #equality
    #to string