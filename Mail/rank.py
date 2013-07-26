import pickle, nltk, math, random
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
			temp += tfidf/math.log(len(line_fd[i]) + 1)


		scores.append((pos[i],temp))

	print sorted(scores,key=itemgetter(1))	

# create a graph file where edges are simple overlap
def createGraph():
	annotPlain = pickle.load(open('sent_400_bi.pickle','rb'))

	posList = []

	for line,sent in annotPlain:
		if sent == 'pos':
			posList.append(line)

	for i,line1 in enumerate(posList):
		for j,line2 in enumerate(posList):
			intersect = len(set(nltk.word_tokenize(line1)) & set(nltk.word_tokenize(line2)))
			if i != j and intersect > 0:
				print i,'\t',j,'\t',intersect


def readRanks():
	annotPlain = pickle.load(open('sent_400_bi.pickle','rb'))

	posList = []

	for line,sent in annotPlain:
		if sent == 'pos':
			posList.append(line)


	ranked = []

	for line in open('graph_out','r').readlines():
		pair = line.split('\t')
		ranked.append((int(pair[0]),float(pair[1])))

	for node,score in sorted(ranked,key=itemgetter(1)):
		print posList[node]

def intersection():
	annotPlain = pickle.load(open('sent_400_bi.pickle','rb'))
	sets = []

	for line,sent in annotPlain:
		if sent == 'pos':
			sets.append(set([a for (a,b) in nltk.pos_tag(nltk.word_tokenize(line.lower())) if 'NN' in b]))

	group(sets)
	for aset in sets:
		print aset


def group(sets):
	over = containsOver(sets)

	if not over:
		return

	i,j = over
	ele1 = sets[i]
	ele2 = sets[j]

	sets.remove(ele1)
	sets.remove(ele2)

	sets.append(ele1|ele2)
	group(sets)


# function to determine if sets in listi 
# contain any overlap
def containsOver(listi):
	for i,ele1 in enumerate(listi):
		for j,ele2 in enumerate(listi):
			if i != j and ele1&ele2:
				return (i,j)
	return None


if __name__ == '__main__':
	readRanks()




