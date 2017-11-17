import pickle
import numpy as np
import operator

fileObject = "curr_write"
fileHandle = open(fileObject,'r')
curr_rept = pickle.load(fileHandle)


fileObject = "prev_write"
fileHandle = open(fileObject,'r')
prev_rept  = pickle.load(fileHandle)


def normalize(number):
	return '{0}'.format(str(number).zfill(4))


fileObject = "bphcTASK2IRLeD.txt"
fileHandle = open(fileObject,'w')

for i in xrange(200):
	print "Writing for file "+str(i)
	ordering = dict()
	ordering[i] = []
	A = np.array(curr_rept[i])
	A = A/np.linalg.norm(A)
	for j in xrange(2000):
		B = np.array(prev_rept[j])
		B = B/np.linalg.norm(B)
		res = np.dot(A,B)
		if res > 0:
			tup = (j,res)
			ordering[i].append(tup)


	temp = ordering[i]
	temp.sort(key=operator.itemgetter(1),reverse = True)
	rank = 1
	stringToBeWritten = ""
	for tup in temp:
		stringToBeWritten =  "current_case_"+normalize(str(i+1))+" Q0 "+ "prior_case_"+normalize(str(tup[0]+1))+" "+str(rank)+" "+str(tup[1])+" bphcTASK2\n"
		rank += 1
		fileHandle.write(stringToBeWritten)