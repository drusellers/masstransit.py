'''
import uuid
from amqplib import client_0_8 as amqp

c = amqp.Connection('172.16.43.141:5672', 'guest', 'guest')
ch = c.connection.connection.channel()
#data, exchange, routing key
#ch.basic_publish('hi','exchange','message:name')
ch.queue_declare(
    queue='myhost.mychannel',
    durable=False,
    exclusive=False,
    auto_delete=True
)
ch.exchange_declare(
    exchange='masstransit',
    type='direct'
)
ch.queue_bind(
    queue='myhost.mychannel',
    exchange='masstransit',
    routing_key='message_name'
)
message = amqp.Message('envelope')
ch.basic_publish(message, 'masstransit','route_it')

def dispatch(message):
	print message.body

ch.basic_consume(
    queue='myhost.mychannel',
    no_ack=True,
    callback=dispatch,
    consumer_tag=str(uuid.uuid4())
)

c.close()
'''
