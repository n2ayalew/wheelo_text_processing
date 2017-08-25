import requests
import csv
import re
import sys, os
from numpy import *
import nltk
import codecs
import tarsqi
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk_contrib.timex import *
import ternip

maxn = 479 # This is the number of rows in the CSV. But we still track the actual number of rows that classified

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

def write_posts_to_file(posts, filename):
	f = open(filename, "w+")
	for msg in posts:
		f.write("\""+msg+"\",Not Labeled,\n")
	f.close()

def get_training_data():
	n, msgs = get_posts('EAACEdEose0cBAPp0YI7oLGqwmqHJZCLdi1enzsDaqYayBZAWjdbwulZBQku0hBPz1OAxVOvjr80OdoQhuER6IMsCGXm3I31uqS24966oddU5kgrraK8Bg7Q3UqZCyH66gO9jnTnkcPuJjD6tnlBqtzw3vz1nawShqKNwfuaTMARVOWoU6haWcXZAfOoCfFj5gtvlya2spBgZDZD')
	write_posts_to_file(msgs, 'training_data/typelabel_training.csv')

def parse_trainning_data():
	f = open("training_data/typelabel_training_labeled.csv", "r")
	reader = csv.reader(f)
	posts = []
	labels = []
	count = 0
	for row in reader:
		posts.append(row[0])
		count+=1
		if (row[1] == 'DRIVER'):
			labels.append(1)
		elif (row[1] == 'RIDER'):
			labels.append(-1)
		elif (row[1] == 'OTHER'):
			labels.append(0)
		else:
			posts.pop()
			count-= 1
	f.close()
	return posts,labels,count

def parse_text(s):
	reg = re.compile("[\"$&+,:;=?@#|_'.^*()%!/]|\s+")
	lst = reg.split(s)
	token_list = [tok.lower() for tok in lst if len(tok) > 0]
	return token_list

def main():
	posts,labels,num_posts = parse_trainning_data()

main()
