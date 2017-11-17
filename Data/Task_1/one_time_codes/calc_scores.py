for i in xrange(100):
	actual = 'gen_actualCatch/'+ 'Doc'+str(i) + '.txt' 
	handle_actual = open(actual,"r")
	actual_set = set()
	for line in handle_actual:
		line = line.split()
		for word in line:
			actual_set.add(word)

	generated = 'gen_keyphrases/'+ 'Doc'+str(i) + '.txt' 
	handle_generated = open(generated,"r")
	generated_set = set()
	for line in handle_generated:
		line = line.split()
		for word in line:
			generated_set.add(word)

	precision = len(actual_set.intersection(generated_set))/float(len(generated_set))
	recall = len(actual_set.intersection(generated_set))/float(len(actual_set))
	print "\nDoc"+str(i)+": \n"
	print "Accuracy: "+ str(precision*100)+"%"
	print "Recall: " + str(recall*100)+"%"
