from celery import Celery
from pprint import pprint
from flask import Flask, jsonify
import time
import json
import os
import swiftclient.client

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=2, **config)

def countTweets():
	(response, object_list) = conn.get_container('tweets')
	master_count = {
		'nr_of_tweets': 0,
		'count_hon': 0,
		'count_han':  0,
		'count_den': 0,
		'count_det': 0,
		'count_denna': 0,
		'count_denne': 0,
		'count_hen': 0
	}
	for object in object_list:
		(object_id,output) = conn.get_object("tweets", object['name'])
		split_str = output.split('\n')
		split_str = filter(None,split_str)
		for item in split_str:
			print item
			json_temp = json.loads(item)
			master_count['nr_of_tweets'] += 1
			check = json_temp['text'].lower()
			master_count['count_hon'] += check.count('hon')
			master_count['count_han'] += check.count('han')
			master_count['count_den'] += check.count('den')
			master_count['count_det'] += check.count('det')
			master_count['count_denna'] += check.count('denna')
			master_count['count_denne'] += check.count('denne')
			master_count['count_hen'] += check.count('hen')
		print("Object {} done!".format(object['name']))

countTweets()
