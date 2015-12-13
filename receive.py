#!/usr/bin/env python
import pika
import time

_output_directory = 'images/'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='starlapse')

def callback(ch, method, properties, body):
	#write file to output directory with timestamp as name
	file_name = str(time.time())
	output_file = open(_output_directory + file_name, "w")
	output_file.write(body)
	print ' Added data to ' + str(file_name)

channel.basic_consume(callback, queue='starlapse', no_ack=True)

print ' [*] Waiting for messages. To exit press CTRL+C'

channel.start_consuming()
