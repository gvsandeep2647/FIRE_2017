for i in xrange(100):
	catchwords = 'Train_catches/case_'+str(i)+'_catchwords.txt'
	cpfile = open(catchwords)

	unique_words = set()
	for line in cpfile:
		words = line.split(', ')
		for j in xrange(len(words)):
			temp = words[j].split()
			for k in xrange(len(temp)):
				unique_words.add(temp[k].lower())

	unique_words = list(unique_words)
	stringToBeWritten = ' '.join(map(str, unique_words)) 

	writeIn = 'gen_actualCatch/' + "Doc"+str(i) + '.txt'
	handle = open(writeIn,"w")
	handle.write(stringToBeWritten) 