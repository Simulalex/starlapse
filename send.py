#!/usr/bin/env python
import pika
import os
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='starlapse')

last_uploaded_file_timestamp = 0
target_image_directory = '/tmp/images/'

def _get_file_to_upload():
	best_time = time.time()
	best_file = None
	for target_file in os.listdir(target_image_directory):
		target_path = target_image_directory + target_file
		found_time = os.stat(target_path).st_ctime

		if best_time > found_time and found_time > last_uploaded_file_timestamp:
			best_time = found_time
			best_file = target_path
	return best_file


#loop forever
while True:
	#get oldest image newer than most recent upload timestamp
	target_path = _get_file_to_upload()
	
	
	#if none, sleep 1 second
	if (target_path is None):
		time.sleep(2)

	#otherwise, publish that image and update most recent upload timestamp
	else:
		target_file = open(target_path, 'r')
		last_uploaded_file_timestamp = os.stat(target_path).st_ctime
		print 'Updated last upload time'
		data = target_file.read()

		channel.basic_publish(exchange='',
			routing_key='starlapse',
			body=data)

connection.close()


