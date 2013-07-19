import pickle,nltk
from numpy import *


def buildMatrix():
	annotPlain = pickle.load(open('sent_400_bi.pickle','rb'))

	bySent = {'pos':[],'neg':[]}


	for line,sent in annotPlain:
		bySent[sent].append(nltk.word_tokenize(line.lower().strip('.')))

	nNeg = len(bySent['neg'])
	nPos = len(bySent['pos'])


	mat = array([0 for x in range(nNeg**2)]).reshape(nNeg,nNeg)

	for i,list1 in enumerate(bySent['neg']):
		for j,list2 in enumerate(bySent['neg']):
			mat[i][j] = pairScore(list1,list2)

	tuples = []
	for i,row in enumerate(mat):
		tuples.append((row.sum()/float(len(bySent['neg'][i])),bySent['neg'][i]))
	
	print sorted(tuples)

def pairScore(list1,list2):
	return len(set(list1) & set(list2))
	
if __name__ == '__main__':
	buildMatrix()