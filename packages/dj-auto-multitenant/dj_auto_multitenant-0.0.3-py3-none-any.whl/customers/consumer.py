import pika, json

from .models import Client
from django.conf import settings


params = pika.URLParameters(settings.CLOUDAMQP_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='new_tenant')

def callback(ch, method, properties, body):
    # print('Received in admin')
    if properties == 'new_client':
        data = json.loads(body)
        # print(id)
    
        client = Client.objects.create(name = data['name'])
        client.save()
    print('Tenant added ')

channel.basic_consume(queue='new_tenant', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
