from celery import Celery
from pprint import pprint
import json
import os
import swiftclient.client
from novaclient.client import Client
import progressbar

def update_progress(progress):
    print '\r[{0}] {1}%'.format('#'*(progress/5), progress)

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=2, **config)

bar = progressbar.ProgressBar(maxval=20, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

import sys

def cli_progress_test(end_val, bar_length=20):
    for i in xrange(0, end_val):
        percent = float(i) / end_val
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
        sys.stdout.flush()

cli_progress_test(5)
cli_progress_test(20)

current_progress = 0
nr_of_tweets = 0
count_hon = 0
count_han = 0
count_den = 0
count_det = 0
count_denna = 0
count_denne = 0
count_hen = 0
(response, object_list) = conn.get_container("tweets")
update_progress(current_progress)
for object in object_list:
	(object_id,output) = conn.get_object("tweets", object['name'])
	split_str = output.split('\n')
	split_str = filter(None,split_str)
	for item in split_str:
		json_temp = json.loads(item)
		nr_of_tweets += 1
		check = json_temp['text'].lower()
		count_hon += check.count('hon')
		count_han += check.count('han')
		count_den += check.count('den')
		count_det += check.count('det')
		count_denna += check.count('denna')
		count_denne += check.count('denne')
		count_hen += check.count('hen')
	#print("Object {} done!".format(object['name']))
#	current_progress += 1
#	bar.update(current_progress)
print("{}{}".format("Number of tweets: ", nr_of_tweets))
print("{}{}".format("Number of 'hon': ", count_hon))
print("{}{}".format("Number of 'han': ", count_han))
print("{}{}".format("Number of 'den': ", count_den))
print("{}{}".format("Number of 'det': ", count_det))
print("{}{}".format("Number of 'denna': ", count_denna))
print("{}{}".format("Number of 'denne': ", count_denne))
print("{}{}".format("Number of 'hen': ", count_hen))
