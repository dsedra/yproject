import pickle, nltk, math
from numpy import *
from operator import itemgetter


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


def tfIDF():
	from nltk.probability import FreqDist, ConditionalFreqDist

	annotPlain = pickle.load(open('sent_400_bi.pickle','rb'))

	# sort based on sent to simulate classification

	total_fd = FreqDist()
	line_fd = []
	tf = {} 
	idf = {}
	pos = []

	for line,sent in annotPlain:
		fd = FreqDist()
		if 'pos' in sent:
			for word in nltk.word_tokenize(line.lower()):
				fd.inc(word)
				total_fd.inc(word)
			line_fd.append(fd)
			pos.append(line)

	for i,stats in enumerate(line_fd):
		for entry in stats:
			tf[(entry,i)] = 0.5 + 0.5*stats[entry]/stats[stats.max()]


	for term in total_fd:
		count = 0
		for dist in line_fd:
			if dist[term] > 0:
				count += 1
		idf[term] = math.log(len(line_fd)/count)

	scores = []

	for i in range(len(line_fd)):
		temp = 0
		for term in line_fd[i]:
			tfidf = tf.get((term,i),0)*idf.get(term,0)
			#scores[term] = scores.get(term,0) + tfidf
			temp += tfidf/float(len(line_fd[i]))


		scores.append((pos[i],temp))

	print sorted(scores,key=itemgetter(1))		


		

	


if __name__ == '__main__':
	tfIDF()