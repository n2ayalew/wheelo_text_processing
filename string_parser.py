import requests
import re
import codecs
from fb_post import FBPost
from round_trip_classifier import RoundTripClassifier
from location_finding2 import LocFinder
from ride_price_finder import get_post_prices
from temporal_gutime import TemporalTagger

# GLOBALS
URL_RIDESHARE = 'https://graph.facebook.com/v2.8/225049564330328/feed' 

def get_posts(token, limit):
	"""
	Get a number of 'limit' posts and initalize a FBPost instance for each one.
	The token param is used to gain privlidges for FB API.
	Returns:
	- List of FBPost instances
	- Size of FBPost list
	- URL of previous pagination for FB Page
	- URL of next in pagination for FB Page
	"""
	url = URL_RIDESHARE + '?limit=' + str(limit) + '&access_token=' + token
	r = requests.get(url)
	j = r.json()
	data = j['data']
	next_posts = j['paging']['next']
	prev = j['paging']['previous']
	messages = []
	up_times = []
	ids = []
	posts = []
	count = 0
	post = ""

	for i in range(0,len(data)):
		msg = data[i]
		if ('message' not in msg):
			continue
		post = ' '.join(msg['message'].split('\n')).encode('utf-8').strip()
		try:
			messages.append(codecs.encode(post, 'utf-8'))
			up_times.append(msg['updated_time'].encode('utf-8'))
			ids.append(msg['id'].encode('utf-8'))
			posts.append(FBPost(messages[-1], up_times[-1], ids[-1]))
			count += 1
		except UnicodeDecodeError:
			continue
	
	return posts, count, prev, next_posts

def type_tagger(num_posts, posts):
	""" 
	Tag each FBPost as either RIDER, DRIVER, or OTHER
	"""
	
	others = []
	rideshare_posts = []
	num_rideshare_posts = 0
	nrs = 0
	for i in range(num_posts):
		posts[i].set_type()
		if (posts[i].driver_post):
			rideshare_posts.append(posts[i])
			nrs += 1
		else:
			others.append(posts[i])
	return rideshare_posts, others, nrs

def rt_tagger(rs_posts, others):
	""" 
	This part should distinguish posts that inidcate round-trips and nonround-trips.
	However, it seems to be distinguishing between posts that have many locations listed and ones that have a standard amount (2)
	"""
	rtClassifier = RoundTripClassifier()
	for rs in rs_posts:
		rs.round_trip = rtClassifier.classify(rs.msg)
	for o in others:
		o.round_trip = rtClassifier.classify(o.msg)
	return rtClassifier

def loc_tagger(rs_posts):
	"""
	Finds the mentioned locations in the post and labels each one as either origin,
	dest or other.
	"""
	lf = LocFinder()
	for rs in rs_posts:
		lf.classifyLocs(rs.msg)
		rs.origin = lf.origins
		rs.dest = lf.dests
		rs.other_locs = lf.others
		lf.resetLocs()

def price_finder(rs_posts):
	"""
	Given a list of FBPosts in UTF-8 encoding, set price member as list of potential post prices.
	"""
	for rs in rs_posts:
		rs.prices = get_post_prices(rs.msg)

def temporal_tagger(rs_posts, n):
	tt = TemporalTagger(rs_posts)
	tt.refresh_all()
	tt.tag_all_posts(rs_posts, n)
	return tt

def main(token):

	posts, nposts, prev_page, next_page = get_posts(token, 50) 

	rs_posts, others, nrs = type_tagger(nposts, posts)

	rtClassifier = rt_tagger(rs_posts, others)

	loc_tagger(rs_posts)

	price_finder(rs_posts)

	tempTagger = temporal_tagger(rs_posts, nrs)

	return


main('EAACEdEose0cBAF4xI2dHK48JVeqV0Yd9HOyYe8q4zDOnJStSBR3M1JMeG4Czk9uYm8mGZAcEKivQzs9U38ZBFJdEiA9GrvI3zQibGZCFj6byNkOmBkTweiT5qs2AWzv8idJ0hytWZBdQVwKZCA1HjltNrDTGGvtg3mCIgPFLZCQRHFKQ8RPW100MkMvyxr6DoZD')
