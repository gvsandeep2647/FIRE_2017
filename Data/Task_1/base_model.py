import string
import math
import re
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
import io
import nltk

#The result obtained after analysing the actual keyphrases and their POS Tags. Used for weighin the terms.
Tagger_dictionary={'MD': 1, 'PRP$': 1, 'VBG': 57, 'JJ': 286, 'NN': 761, 'VBD': 37, 'CC': 2, 'RBR': 2, 'JJS': 3, 'VB': 16, 'VBN': 27, 'TO': 1, 'VBP': 40, 'PRP': 1, 'RB': 21, 'IN': 24, 'VBZ': 10, 'DT': 4, 'CD': 1, 'NNS': 56, 'JJR': 1}

#Normalisingg the values so as to use them for wighing
for key,value in Tagger_dictionary.iteritems():
	Tagger_dictionary[key]=value/761.0
weight_tags=100

database = {}
vocabulory = set()
freqTable = {}
word_thresh={}

def setupDatabase():

	'''
	Sets up the vocabulory in a format such that calculating all the scores become easy
	'''
	for i in xrange(400):
		try:
			print "adding to database", i
			finalString = ""
			if(i<100):
				doc = 'Train_docs/case_'+str(i)+'_statement.txt'
			else:
				doc= 'Test_docs/case_'+str(i)+'_statement.txt'
			docFile = open(doc)
			content = ""
			document = ""
			for line in docFile:
				content += line.strip().lower()+" "
				document += line.strip().lower()+" "

			content = word_tokenize(content)

			for j in xrange(len(content)):
				content[j] = re.sub('[(!@#$-./-_,")]', '', content[j]).strip() # Removing Punctuation. Anything which matches the regEx will be replaced with null character

			content = filter(None, content) # Removing Empty strings
			
			content = list(set(content))
			content=[word for word in content if word not in stopwords.words('english') and len(word)>4]
			word_freq = {}
			for word in content:
				vocabulory.add(word)
				word_freq[word] = document.count(word)
			unique_cp = set()
			if(i<100):
				''' Making the Set of unique Catch Words '''	
				
				catchwords = 'Train_catches/case_'+str(i)+'_catchwords.txt'
				cpfile = open(catchwords)
				
				for line in cpfile:
					words = line.split()
				for word in words:
					word = word.lower()
					word = re.sub('[(!@#$-./-_,)"]', '', word)
					unique_cp.add(word)
			database[i] = [word_freq,unique_cp]
		except Exception as e:
			print e
	print len(vocabulory)
	for word in vocabulory:
		freqTable[word] = []
		for I in xrange(len(database)):
			try:
				i=I+100 							#necessary for mapping to right index of file
				presence = 0
				count = 0
				if word in database[i][0]:
					count = database[i][0][word]
				if word in database[i][1]:
					presence = 1
				if count > 0:
					sublist = [0,0]
					sublist[0],sublist[1] = count , presence
					freqTable[word].append(sublist)
			except:
				pass

def Fcfound(t):
	numerator=0.0
	denom=0.0
	for i in xrange(100,400):
		try:
			dic=database[i][0]
			cp=database[i][1]
			if(t in dic):
				denom+=1
				if(t in cp):
					numerator+=1
		except:
			pass
	return numerator/denom

def Fcfoundfreq(t,i): #in ith document
	return Fcfound(t)*(database[i][0][t])

def Freqmedia(t,i): # in ith doc
	total_occurrence=0.0
	for j in xrange(100,400):
		try:
			if( t in database[j][0]):
				total_occurrence+=database[j][0][t]
		except:
			pass
	occurrence_cur=0.0
	if(t in database[i][0]):
		occurrence_cur=database[i][0][t]
	return (occurrence_cur*300)/total_occurrence

def TFIDF(t,i):
	NDocs_t=0.0
	for j in xrange(100):
		try:
			if(t in database[j][0]):
				NDocs_t+=1
		except:
			pass
	if(t not in database[i][0]):
		return 0
	try:
		return database[i][0][t]*math.log(100.0/(NDocs_t))
	except:
		return 0


def getThreshold(word): #assumes word is present in vocabulary

	'''
	For all words which gives the threshold for which it is highly likely that it will be present in both the document as well as the kepywords
	'''
	if(word not in freqTable):
		return 1000000000000 #ignore word by setting very high threshold if word isnt present in training docs
	if(len(freqTable[word])==0):
		return None
	best_thresh=freqTable[word][0]
	best_error=1000000000000 #infinity

	for pair in freqTable[word]:
		current_thresh=pair[0]
		error=0
		for iter_pair in freqTable[word]:
			if(iter_pair[0] < current_thresh and iter_pair[1]==1):
				error+=1
			if(iter_pair[0] >= current_thresh and iter_pair[1]==0):
				error+=1
		if(error < best_error):
			best_error=error
			best_thresh=current_thresh

	return best_thresh

def getPOSweight(word):
	try:
		return Tagger_dictionary[nltk.pos_tag([word])[0][1]]*weight_tags
	except:
		# print "error while pos tagging ", word
		return 0
	

def convert():
	for i in xrange(400):
		try:
			finalString = ""
			if( i< 100):
				doc = 'Train_docs/case_'+str(i)+'_statement.txt'
			else:
				doc = 'Test_docs/case_'+str(i)+'_statement.txt'

			docFile = io.open(doc,'r',encoding='utf-8',errors='ignore')
			content = ""
			document = ""
			for line in docFile:
				content += line.strip().lower()+" "
				document += line.strip().lower()+" "

			print "Converting ",i
			content = word_tokenize(content)
			for j in xrange(len(content)):
				content[j] = re.sub('[(!@#$-./-_,")]', '', content[j]).strip() # Removing Punctuation. Anything which matches the regEx will be replaced with null character
			
			content = filter(None, content) # Removing Empty strings
			
			content = list(set(content))
			
			word_freq = {}
			for word in content:
				vocabulory.add(word)
				word_freq[word] = document.count(word)
			
			stringToBeWritten = ""
			writeIn = 'shortened/' + "Doc"+str(i) + '.txt' 
			handle = io.open(writeIn,'w',encoding='utf-8',errors='ignore')

			docFile_new=open(doc)
			raw_data=docFile_new.read()
			sentence_list=sent_tokenize(raw_data)

			for line in sentence_list:
				line=line.lower().strip()
				line=re.sub('[(!@#$-./-_,")]', '', line).split()
				length=len(stringToBeWritten)	
				for word in line:
					if(word!=''):
						if(word[-1]=='.'): #if this word is the ending word for sentence
							word=word[:-1]
						try:
							if(word_freq[word]+getPOSweight(word) >= getThreshold(word)):
								stringToBeWritten=stringToBeWritten+word+' '
						except Exception as exc:
							# print exc
							pass
				length=len(stringToBeWritten)-length
				if(length>0):
					stringToBeWritten+='. '
			
			handle.write(unicode(stringToBeWritten))
			print "Converted", i
		except Exception as e:
			print e

setupDatabase()
# convert()