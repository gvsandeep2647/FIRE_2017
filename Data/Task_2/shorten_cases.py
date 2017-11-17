import pickle
import io
import re
from math import log
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import operator

corpus = dict()
tags={'MD': 1, 'PRP$': 1, 'VBG': 57, 'JJ': 286, 'NN': 761, 'VBD': 37, 'CC': 2, 'RBR': 2, 'JJS': 3, 'VB': 16, 'VBN': 27, 'TO': 1, 'VBP': 40, 'PRP': 1, 'RB': 21, 'IN': 24, 'VBZ': 10, 'DT': 4, 'CD': 1, 'NNS': 56, 'JJR': 1}
total = 0
for key in tags:
	total += tags[key]
for key,value in tags.iteritems():
	tags[key]=value/float(total)

weight = dict()
def calc_weight():
	global corpus,weight

	for word in corpus:
		weight[word] = (1 + log(200.0/len(corpus[word])))
	for word in weight:
		temp = [word]
		tag = nltk.pos_tag(temp)[0][1]
		if tag in tags:
			weight[word] = weight[word] * tags[tag]
		else:
			weight[word] = weight[word] * 0

def openCase(filename):
	global corpus

	fileHandle = io.open(filename,'r',encoding='utf-8',errors='ignore')
	content = ""
	for line in fileHandle:
		content += line.strip().lower()+" "
	content = word_tokenize(content)
	for j in xrange(len(content)):
		content[j] = re.sub('[(!@#$-./-_,")]', '', content[j]).strip()
			
	content = filter(None, content)
	document = content			
	content = list(set(content))
	content = [word for word in content if word not in stopwords.words('english') and len(word)>4]
	for word in content:
		if word in corpus:
			corpus[word].append(document.count(word))
		else:
			corpus[word] = []
			corpus[word].append(document.count(word))



def normalize(number):
	return '{0}'.format(str(number).zfill(4))


for i in xrange(200):
	filename = 'Current_Cases/current_case_'+str(normalize(i+1))+'.txt'
	print "Working on case" + str(normalize(i+1))
	openCase(filename)
	calc_weight()

sorted_weight = sorted(weight.items(),reverse=True, key=operator.itemgetter(1))
sorted_weight = sorted_weight[:5000]

weight = {}
ordering = {}
count = 0
for tup in sorted_weight:
	ordering[tup[0]] = count
	count += 1
for tup in sorted_weight:
	weight[tup[0]] = tup[1]

curr_cases = {}
for i in xrange(200):
	filename = 'Current_Cases/current_case_'+str(normalize(i+1))+'.txt'
	vector = [0]*5000
	fileHandle = io.open(filename,'r',encoding='utf-8',errors='ignore')
	content = ""
	for line in fileHandle:
		content += line.strip().lower()+" "
	content = word_tokenize(content)
	for j in xrange(len(content)):
		content[j] = re.sub('[(!@#$-./-_,")]', '', content[j]).strip()
			
	content = filter(None, content)
	content = [word for word in content if word not in stopwords.words('english') and len(word)>4]
	print "Vectorizing case" + str(normalize(i+1))
	for word in ordering:
		vector[ordering[word]] = weight[word] * content.count(word)
	curr_cases[i] = vector

curr_write = "curr_write"
fileObject = open(curr_write,'wb')
pickle.dump(curr_cases,fileObject)

order = "ordering"
fileObject = open(order,'wb')
pickle.dump(ordering,fileObject)