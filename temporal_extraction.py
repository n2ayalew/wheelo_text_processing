import requests
import re
from numpy import *
import nltk
import codecs
from nltk_contrib.timex import *
import ternip

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
	return dates, ne_chunks

def test_temporal_extracter(token):
	num_posts, posts = get_posts(token)

	for p in posts:
		print "-----------------------------NEW POST----------------------------------\n"
		timex_tagged, chunks = get_date_time(p)
		#print timex_tagged + "\n\n"
		print "-----------------------------END POST----------------------------------\n"
test_temporal_extracter('EAACEdEose0cBANVIj3BIkhbQaFpwDZC8UhPIMAb3MlGRXBO7RLNtanLl54aYE9zqIgxAwHfXA1U2NOlIUkYecjOlaUQtPMYXcRjZBJP6WztsVw5zKrEtZB21iZCclsXJvK0cTpK2pedreaEkFaRYRMUhdG39TFIbGbrLTxxfKFEZCJZBNCO1V3unhZAROWI6adZAN2UxuZCs0LAZDZD')
