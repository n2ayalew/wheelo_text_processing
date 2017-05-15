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

def parse_trainning_data():
	f = open("training_data.txt", "r")
	posts = []
	labels = []
	for line in f:
		if (line != "\n" and (line.find("ROUND TRIP") != -1)):
			line_parts = line.split("ROUND TRIP:")
			post = parse_text(line_parts[0].strip("{").strip())
			posts.append(post)
			labels.append(float(line_parts[1].strip("}\n").strip()))
	return posts,labels

def parse_text(s):
	reg = re.compile("[\"$&+,:;=?@#|_'.^*()%!/]|\s+")
	lst = reg.split(s)
	token_list = [tok.lower() for tok in lst if len(tok) > 0]
	return token_list

def main():
	posts, labels = parse_trainning_data()
	vocab = build_vocab(posts)

	# vectorize posts
	post_vecs = []
	for p in posts:
		vec = convert_words_to_vec(p, vocab)
		post_vecs.append(vec)
	
	# get 50 random posts for test data
	training_set = range(500)
	test_list = []

	for i in range(50):
		rand_index = int(random.uniform(0, len(training_set)))
		test_list.append(training_set[rand_index])
		del(training_set[rand_index])

	training_posts = []
	training_labels = []

	for i in training_set:
		training_posts.append(post_vecs[i])
		training_labels.append(labels[i])

	p1,p0,p1Vec,p0Vec = trainNB(array(training_posts), array(training_labels))

	# Test classifier
	error_rate = 0.0
	for i in test_list:
		label = classifyNB(post_vecs[i], p0Vec, p1Vec, p0, p1)
		if (label != labels[i]):
			error_rate += 1
	error_rate /= 50
	print error_rate

main()
