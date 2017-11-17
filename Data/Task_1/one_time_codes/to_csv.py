for i in xrange(99):
	finalString = ""
	doc = 'Train_docs/case_'+str(i)+'_statement.txt'
	catchwords = 'Train_catches/case_'+str(i)+'_catchwords.txt'

	docFile = open(doc)
	for line in docFile:
		finalString += line.strip()

	finalString += "@@"

	catchFile = open(catchwords)
	for line in catchFile:
		finalString += line.strip()

	print finalString