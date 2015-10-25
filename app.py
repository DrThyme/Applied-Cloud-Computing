from celery import Celery, group, subtask
from pprint import pprint
from flask import Flask, jsonify
import sys
import time
import json
import os
import swiftclient.client

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'amqp'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=2, **config)

def workerCount(tweets):
	count = {
		'#tweets': 0,
		'hon': 0,
		'han':  0,
		'den': 0,
		'det': 0,
		'denna': 0,
		'denne': 0,
		'hen': 01
	}
	split_tweets = tweets.split('\n')
	split_tweets = filter(None,split_tweets)
	for tweet in split_tweets:
		print tweet
		json_temp = json.load(tweet)
		if not json_temp['retweeted']:
			master_count['#tweets'] += 1 
			check = json_temp['text'].lower() 
			count['hon'] += check.count('hon') 
			count['han'] += check.count('han') 
			count['den'] += check.count('den') 
			count['det'] += check.count('det') 
			count['denna'] += check.count('denna') 
			count['denne'] += check.count('denne') 
			count['hen'] += check.count('hen')
	return(count)

def sum_counts(master,results):
	for result in results:
		master['#tweets'] += result['#tweets']
		master['hon'] += result['hon']
		master['han'] += result['han']
		master['den'] += result['den']
		master['det'] += result['det']
		master['denna'] += result['denna']
		master['denne'] += result['denne']
		master['hen'] += result['hen']
	return(master)


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

@celery.task
def check_tweet(object_name):
	print "==== Worker fetching file:", str(object_name), "===="
	(object_id,output) = conn.get_object("tweets", object_name)
	workerResult = workerCount(output)
	print "==== Worker count on file:", str(object_name), "- COMPLETE! ===="
	return(workerResult)

@app.route('/', methods=['GET'])
def display_info():
	return "Welcome! In order to get to the application, please navigate to /run"

@app.route('/run', methods=['GET'])
def allocate_tasks():
	master_count = {
		'#tweets': 0,
		'hon': 0,
		'han':  0,
		'den': 0,
		'det': 0,
		'denna': 0,
		'denne': 0,
		'hen': 0
	}
	(response, obj_list) = conn.get_container('tweets')
	object_name_list = []
	for object in obj_list:
		object_name_list.append(object['name'])

	tasks = [check_tweet.s(object_name) for object_name in object_name_list]
	t_group = group(tasks)
	results = t_group()

	while not results.ready():
		time.sleep(5)
		completed = results.completed_count()
		text = "\rProgress: {0}/20 subtasks done".format(completed) 
		sys.stdout.write(text)
		sys.stdout.flush()

	print "ALL SUBTASKS COMPLETE"
	master_count = sum_counts(master_count,results.get())
	return jsonify(master_count)

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
