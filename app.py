from celery import Celery
from pprint import pprint
import json
import os
import swiftclient.client

config = {'username':os.environ['OS_USERNAME'], 
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=2, **config)

app = Flask(__name__)
worker = Celery(app.name, backend='amqp', broker='amqp://')

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

def workerCount(tweets):
	split_tweets = tweets.split('\n')
	split_tweets = filter(None,split_tweets)
	for tweet in split_tweets:
		json_temp = json.load(item)
		if not json_temp['retweeted']:
			master_count['nr_of_tweets'] += 1 
            check = json_temp['text'].lower() 
            master_count['count_hon'] += check.count('hon') 
            master_count['count_han'] += check.count('han') 
            master_count['count_den'] += check.count('den') 
            master_count['count_det'] += check.count('det') 
            master_count['count_denna'] += check.count('denna') 
            master_count['count_denne'] += check.count('denne') 
            master_count['count_hen'] += check.count('hen')
	

def countTweets(object_list):
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

@worker.task
def check_tweet(object_name):
	print "==== Worker fetching file:", str(object_name), "===="
	(object_id,tweets) = conn.get_object("tweets", object_name['name'])
	workerCount(tweets)
	print "==== Worker count on file:", str(object_name), "- COMPLETE! ===="

@app.route('/', methods['GET'])
def display_info():
	print "Welcome!"
	print "In order to get to the application, please navigate to /run"

@app.route('/run', methods['GET'])
def allocate_tasks():
	
	(response, obj_list) = conn.get_container('tweets')
	object_name_list = []
	for object in obj_list:
		object_name_list.append(object['name'])

	tasks = 
