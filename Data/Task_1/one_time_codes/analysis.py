totalCP = 0
foundCP = 0
unfoundCP = []

print "\n\n\n***** Document Level Analysis *****\n\n\n"
for i in xrange(99):
	finalString = ""
	doc = 'Train_docs/case_'+str(i)+'_statement.txt'
	catchwords = 'Train_catches/case_'+str(i)+'_catchwords.txt'

	docFile = open(doc)
	content = ""
	for line in docFile:
		content += line.strip().lower()

	catchFile = open(catchwords)
	words = []
	for line in catchFile:
		words += line.split(',')
	
	for i in xrange(len(words)):
		words[i] = words[i].strip().lower()


	for word in words:
		totalCP = totalCP + 1
		if word in content:
			foundCP = foundCP + 1
		else:
			unfoundCP.append(word)

print "Total CatchPhrases = "+ str(totalCP) + "\nFound CatchPhrases =  " + str(foundCP)+"\nUnfound CatchPhrases = " +str(len(unfoundCP))
print "\n\n\n"
print unfoundCP

print "\n\n\n***** Corpus Level Analysis *****\n\n\n"


totalCP = 0
foundCP = 0
unfoundCP = []

content = ""
words = []
for i in xrange(99):
	finalString = ""
	doc = 'Train_docs/case_'+str(i)+'_statement.txt'
	catchwords = 'Train_catches/case_'+str(i)+'_catchwords.txt'

	docFile = open(doc)
	for line in docFile:
		content += line.strip().lower()

	catchFile = open(catchwords)
	for line in catchFile:
		words += line.split(',')
	
for i in xrange(len(words)):
	words[i] = words[i].strip().lower()

for word in words:
	totalCP = totalCP + 1
	if word in content:
		foundCP = foundCP + 1
	else:
		unfoundCP.append(word)

print "Total CatchPhrases = "+ str(totalCP) + "\nFound CatchPhrases =  " + str(foundCP)+"\nUnfound CatchPhrases = " +str(len(unfoundCP))
print "\n\n\n"
print unfoundCP