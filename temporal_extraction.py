import requests
import re
from numpy import *
import nltk
import codecs
from nltk_contrib.timex import *

def get_posts(token):
	r = requests.get("https://graph.facebook.com/v2.8/225049564330328/feed?limit=500&access_token=" + token)
	j = r.json()
	data = j['data']
	next_posts = j['paging']['next']
	prev = j['paging']['previous']
	messages = []
	post = ""
	for msg in data:
	#	print "<---------------------- POST # " + str(i) + " ----------------------->\n"
		if ('message' not in msg):
			continue
		post = ' '.join(msg['message'].split('\n')).encode('utf-8').strip()
		try:
			messages.append(codecs.encode(post, 'utf-8'))
		except UnicodeDecodeError:
			continue
	return len(messages), messages

def get_date_time(p):
	# chunking
	tokens = nltk.word_tokenize(p)
	tags = nltk.pos_tag(tokens)
	ne_chunks = nltk.chunk.ne_chunk(tags)
	# timex tagging
	tags = tag(p)
	dates = ground(tags, gmt())
	return dates

def test_temporal_extracter(token):
	num_posts, posts = get_posts(token)

	for p in posts:
		'-----------------------------NEW POST ----------------------------------'
		print get_date_time(p) + '\n\n'

test_temporal_extracter('EAACEdEose0cBABlK8ORHZCm24WRUsLz8UVKSSXMjL0agkLtE15rnIcH4dhv33TZBmdUZBqO4YvkjCfjRstjzCCLO1TxJG786gQiJx3xxpxYzPLkTZAjlEWVThnPskLWVmpy1ZAB6hZAmbeOR00eNPZBl4QP7gOJu2bA5GXO2ZBRMRWFtlZAsEEl8ZC')
