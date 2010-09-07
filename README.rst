def do_stuff(msg):
    pass

cfg = Config()
bus = Bus(cfg)
bus.Subscribe('message.name', do_stuff)

class SomeMessage:
    def __init__(self):
        pass

bus.publish(SomeMessage())
