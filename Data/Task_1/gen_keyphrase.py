import string
import re
import base_model
from operator import itemgetter
shortened_folder="./shortened"
# number_of_files=200
Name_of_scheme = "bphc_withPOS" 

for i in xrange(100,400):
	# try:
	writeIn='keywords/Output.txt'
	try:
		print i
		file_path=shortened_folder+"/Doc"+str(i)+".txt"
		content=""
		doc=""
		with open(file_path,'r') as F:
			for line in F:
				content+=line
				doc+=line
			
		content=content.split('.')
		
		for j in xrange(len(content)):
			content[j] = re.sub('[(!@#$-./-_,)"]', '', content[j]).strip()


		content = filter(None, content)
		#content is now a list of sentences in the document.
		# print content
		top_ten=[] #list of top_ten words in doc
		word_freq={}
		for sentence in content:
			sentence=sentence.split()
			for word in sentence:
				if(word in word_freq):
					continue
				freq=doc.count(word)
				word_freq[word]=freq


		candidate_words=sorted(word_freq,key=word_freq.get,reverse=True)
		top_ten=candidate_words[:10]
		# print top_ten
		S=[]
		for sentence in content:
			for popular_word in top_ten:
				if(popular_word in sentence):
					S.append(sentence)
		
		candidate_words=[]
		
		for sentence in S:
			sentence=sentence.split()
			for term in sentence: 
				if word_freq[term]>1:
					candidate_words.append(term)
		# print candidate_words
		candidate_words=set(candidate_words)
		word_score=[]
		for word in candidate_words:
			Noccur_in_S=0
			for sentence in S:
				Noccur_in_S+=sentence.count(word)

			score=base_model.TFIDF(word,i)+word_freq[word]+Noccur_in_S
			word_score.append((word,score))
		word_score=sorted(word_score,key=itemgetter(1),reverse=True)
		highest=word_score[0][1]*1.0
		word_score=[(x[0],x[1]/(highest)) for x in word_score]
		with open(writeIn,'a') as handle:
			write_this=Name_of_scheme+"||case_"+str(i)+"_statement||"
			for word , score in word_score:
				write_this+= word+":"+str(score)+","
			write_this=write_this[:len(write_this)-1]+'\n'
			handle.write(write_this)
	except Exception as e:
		print(e)
		with open(writeIn,'a') as handle:
			write_this=Name_of_scheme+"||case_"+str(i)+"_statement||\n"
			handle.write(write_this)
		print i, "not generated"