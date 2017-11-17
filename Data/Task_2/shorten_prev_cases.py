import pickle
import io
import re
from math import log
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import operator

fileObject = "ordering"
fileHandle = open(fileObject,'r')

ordering = pickle.load(fileHandle)

def normalize(number):
	return '{0}'.format(str(number).zfill(4))

prev_cases = dict()
for i in xrange(2000):
	filename = 'Prior_Cases/prior_case_'+str(normalize(i+1))+'.txt'
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
		vector[ordering[word]] = log(1+content.count(word))
	prev_cases[i] = vector

prev_write = "prev_write"
fileObject = open(prev_write,'wb')
pickle.dump(prev_cases,fileObject)