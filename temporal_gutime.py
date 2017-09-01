import requests
import re
import sys, os
import shutil
from numpy import *
import nltk
import codecs
import tarsqi
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk_contrib.timex import *
import ternip

def get_posts(token):
	r = requests.get("https://graph.facebook.com/v2.8/225049564330328/feed?limit=50&access_token=" + token)
	j = r.json()
	data = j['data']
	next_posts = j['paging']['next']
	prev = j['paging']['previous']
	messages = []
	post = ""
	for i in range(0,len(data)):
		msg = data[i]
	#	print "<---------------------- POST # " + str(i) + " ----------------------->\n"
		if ('message' not in msg):
			continue
		post = ' '.join(msg['message'].split('\n')).encode('utf-8').strip()
		try:
			messages.append(codecs.encode(post, 'utf-8'))
		except UnicodeDecodeError:
			continue
	return len(messages), messages

def get_date_time(in_file, out_file):
	options = ["--pipeline", "TOKENIZER,TAGGER,GUTIME", "fb_post_files/in_files/" + in_file, "fb_post_files/out_files/" + out_file]
	tarsqi.run_tarsqi(options)
	return

def build_in_files(posts):
	n = len(posts)
	i = 0

	while (i < n):
		post = posts[i].replace('&', '&amp;') 
		f = open("fb_post_files/in_files/post%s.xml" % i, "w")
		f.write('<?xml version="1.0"?>\n')
		f.write("<TEXT>\n")

		try:
			f.write(post)
		except TypeError:
			sys.exit('ERROR: ' + str(sys.exc_value))

		f.write("\n</TEXT>\n")
		f.close()
		f = 0
		i += 1

def get_date_time_all_posts():
	options = ["--pipeline", "TOKENIZER,TAGGER,CHUNKER,GUTIME", "fb_post_files/in_files/", "fb_post_files/out_files/"]
	tarsqi.run_tarsqi(options)

def refresh_in_files():
	num_posts, posts = get_posts("EAACEdEose0cBAF4xI2dHK48JVeqV0Yd9HOyYe8q4zDOnJStSBR3M1JMeG4Czk9uYm8mGZAcEKivQzs9U38ZBFJdEiA9GrvI3zQibGZCFj6byNkOmBkTweiT5qs2AWzv8idJ0hytWZBdQVwKZCA1HjltNrDTGGvtg3mCIgPFLZCQRHFKQ8RPW100MkMvyxr6DoZD")
	posts = posts[1:]

	dir_in_list = os.listdir("fb_post_files/in_files/")

	for i in dir_in_list:
		os.remove("fb_post_files/in_files/%s" % i)

	# build input files
	build_in_files(posts)

def refresh_in_out_files():
	dir_list = os.listdir("fb_post_files/out_files/")
	for i in dir_list:
		os.remove("fb_post_files/out_files/%s" % i)
	
	refresh_in_files()
	get_date_time_all_posts()
	return


# get time and date info from output
# tag: TIMEX3
# attribute1: type=DATE or type=TIME
# attribute2: value=year+month+day or type=T+24time

def get_post_temp_tags(postid, pwd):
	temp_tags = {"dates":[], "times":[]}
	chunked_dt = []
	try:
		f = open( pwd+'/fb_post_files/out_files/post%s.xml' % postid, "r")
	except IOError, e:
		print str(e)
		return
		
	contents = f.read()
	soup = BeautifulSoup(contents, 'xml')
	timex_tags = soup.find_all('TIMEX3') # WE'LL KEEP ALL THREE SEARCH TEMPORARY UNTIL WE COMPLETE SUFFCICENT TESTING
	dates = soup.find_all(type='DATE')
	times = soup.find_all(type='TIME')
	chunks = soup.find_all(origin='CHUNKER')
	msg = soup.text.encode('utf-8')	
	temp_tags['dates'] = [(d.get('value').encode('utf-8'), msg[int(d.get('begin').encode('utf-8')):int(d.get('end').encode('utf-8'))+1]) for d in dates]
	temp_tags['times'] = [(t.get('value').encode('utf-8'), msg[int(t.get('begin').encode('utf-8')):int(t.get('end').encode('utf-8'))+1]) for t in times]
	temp_tags['times'].append(re.compile('\d+[:|.]\d{2}[ap]m|\d+[ap]m', re.IGNORECASE).findall(msg))	
	for c in chunks:
		i = int(c.get('begin'))
		f = int(c.get('end'))
		chunked_dt.append((msg[i:f+1], i, f))

	
	return temp_tags


# Get tags from all posts
def get_all_posts_temp_tags(n, pwd):
	i = 0
	return [get_post_temp_tags(i, pwd) for i in range(n)]

class TemporalTagger:
	
	def __init__(self, posts):
		self.posts = []
		self.tags = []
		self.curdir = os.getcwd()
		for p in posts:
			self.posts.append(p.msg)
	
	def refresh_all(self):
		shutil.rmtree('fb_post_files/out_files')
		build_in_files(self.posts)
		get_date_time_all_posts()
	
	def tag_all_posts(self, posts, n):
		self.tags = get_all_posts_temp_tags(n, self.curdir)
		for i in range(n):
			posts[i].temporal_tags = self.tags[i]
			posts[i].times = self.tags[i]['times']
			posts[i].dates = self.tags[i]['dates']

def test_tagger(refresh):
	if (refresh):
		refresh_in_out_files() # Refresh all files

	n = len(os.listdir(os.getcwd()+'/fb_post_files/out_files/'))
	lst = get_all_posts_temp_tags(n)
	i = 0
	for tag in lst:
		print 'post' + str(i) + '.xml'
		print tag
		print '\n\n'
		i +=1
