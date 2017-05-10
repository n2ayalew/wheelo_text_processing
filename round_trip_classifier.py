from pprint import pprint
import requests
import re
from numpy import *

# 1 => round trip
# 0 => not round trip

def build_vocab(data_set):
	vocab = set()
	for sample in data_set:
		vocab.update(sample)
	return list(vocab)

def convert_words_to_vec(sample, vocab):
	length = len(vocab)
	word_vec = zeros(length)
	for word in sample:
		if (word in vocab):
			word_vec[vocab.index(word)] += 1
	return word_vec

def trainNB(train_matrix, train_classes):
	num_samples = len(train_matrix)
	num_words = len(train_matrix[0])
	p1 = sum(train_classes)/float(num_samples)
	p0 = 1.0 - p1
	pwi1 = ones(num_words)
	pwi2 = ones(num_words)
	pwi1Denom = 2.0
	pwi2Denom = 2.0

	for i in range(num_samples):
		if (train_classes[i] == 1):
			pwi1 += train_matrix[i]
			pwi1Denom += sum(train_matrix[i])
		else:
			pwi2 += train_matrix[i]
			pwi2Denom += sum(train_matrix[i])

	p1Vec = log(pwi1 / pwi1Denom)
	p0Vec = log(pwi2 / pwi2Denom)
	return p1,p0,p1Vec,p0Vec

def classifyNB(vec2_classify, p0Vec, p1Vec, p0, p1):
	c1 = sum(vec2_classify * p1Vec) + log(p1)
	c0 = sum(vec2_classify * p0Vec) + log(p0)
	if (c1 > c0):
		return 1
	else:
		return 0

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

def write_posts_to_file(posts, filename):
	f = open(filename, "w+")
	for msg in posts:
		f.write(msg + " {ROUND TRIP: }\n\n")
	f.close()

num_posts, posts = get_posts("EAACEdEose0cBACyUYdbbczJIea8Kk9PaYjI34LLyzGkuLSpZCG57ZAoWPC4TB6ZBFqZBC38Dyh6IaZAaXozS4rZCkdgRmDS180jkzvdxZAb1t6v7n5LVm1O2ic7KcMZCE0bKxrUXVzg7Q50zGQpCZARzJXHt1W1nfagtZB2qpIbo1alqoGNxG3lNFe")
print num_posts
write_posts_to_file(posts, "training_data.txt")
