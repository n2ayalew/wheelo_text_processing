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
		messages.append(post)
	return len(messages), messages

def get_post_prices(post):
	"""
	Given a post in UTF-8 encoding return a list of prices found
	"""
	reg = re.compile('\$\s?\d+|\d+\s?\$')
	matches = re.findall(reg, post)

	if len(matches) < 1:
		return ['N/A']
	
	matches = list(set([float(m.strip('$')) for m in matches]))
	return matches

def test_post_price_getter(token):
	num_posts, posts = get_posts(token)

	for p in posts:
		print get_post_price(p)

