import requests
import re
from numpy import *
import nltk
import codecs

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
	# Use ttk script to extract date and time info
	# Need to modify script so we can just import a module and call functions for temporal extraction

def test_temporal_extracter(token):
	num_posts, posts = get_posts(token)

	for p in posts:
		print "-----------------------------NEW POST----------------------------------\n"
		timex_tagged = get_date_time(p)
		print timex_tagged + "\n\n"
		print "-----------------------------END POST----------------------------------\n"

