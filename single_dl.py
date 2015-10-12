from celery import Celery
from pprint import pprint
import json
import os
import swiftclient.client
from novaclient.client import Client

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=2, **config)
app = Celery('tasks', backend='amqp', broker='amqp://')

counts = {
	'nr_of_tweets': 0,
	'count_hon': 0,
	'count_han':  0,
	'count_den': 0,
	'count_det': 0,
	'count_denna': 0,
	'count_denne': 0,
	'count_hen': 0
}

(response, object_list) = conn.get_container("tweets")

@app.task(ignore_result=True)
def countTweets(object_list):
	for object in object_list:
		(object_id,output) = conn.get_object("tweets", object['name'])
		split_str = output.split('\n')
		split_str = filter(None,split_str)
		for item in split_str:
			json_temp = json.loads(item)
			counts['nr_of_tweets'] += 1
			check = json_temp['text'].lower()
			counts['count_hon'] += check.count('hon')
			counts['count_han'] += check.count('han')
			counts['count_den'] += check.count('den')
			counts['count_det'] += check.count('det')
			counts['count_denna'] += check.count('denna')
			counts['count_denne'] += check.count('denne')
			counts['count_hen'] += check.count('hen')
		print("Object {} done!".format(object['name']))
	#print("{}{}".format("Number of tweets: ", nr_of_tweets))
	#print("{}{}".format("Number of 'hon': ", count_hon))
	#print("{}{}".format("Number of 'han': ", count_han))
	#print("{}{}".format("Number of 'den': ", count_den))
	#print("{}{}".format("Number of 'det': ", count_det))
	#print("{}{}".format("Number of 'denna': ", count_denna))
	#print("{}{}".format("Number of 'denne': ", count_denne))
	#print("{}{}".format("Number of 'hen': ", count_hen))
	
	print(counts)

countTweets(object_list)
