# use score tuple to score reviews in a svm
import parse, pickle, nltk

def svm():
	# load the sentiment score file with (word,pos) -> (posScore,negScore) dictionary
	# and the (review,sentiment) pair list
	synDict = pickle.load(open('sentiment_score.pickle','rb'))
	revs = pickle.load(open('review_sent.pickle','rb'))

	keyList = map(lambda (a,b):a,synDict.keys())
	print 'too' in keyList
	count = 0
	scores = {'pos':[],'neg':[],'neut':[],'both':[]}

	for (rev,sent) in revs:
		scoreList = []
		found = False
		for (word,pos) in nltk.pos_tag(nltk.word_tokenize(rev.lower())):
			#if 'JJ' in pos and (word,'a') in synDict:
			#	scoreList.append(synDict[(word,'a')])
			#elif 'NN' in pos and (word,'n') in synDict:
			#	scoreList.append(synDict[(word,'n')])
			#elif 'V' in pos and (word,'v') in synDict:
			#	scoreList.append(synDict[(word,'v')])
			if (word,'a') in synDict or (word,'v') in synDict or (word,'n') in synDict or (word,'r') in synDict:
				found = True

		if not found:
			count += 1
			print rev,sent
		#if len(scoreList) != 0:
		#	scores[sent].append(reduce(lambda (a,b),(c,d):(a+c,b+d), scoreList))

	#print map (lambda (a,b):b, scores['neut'])
	print count




		
if __name__ == '__main__':
	svm()