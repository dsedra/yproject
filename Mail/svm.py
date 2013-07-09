# use score tuple to score reviews in a svm
import parse, pickle, nltk, negate

def svm():
	# load the sentiment score file with (word,pos) -> (posScore,negScore) dictionary
	# and the (review,sentiment) pair list
	synDict = pickle.load(open('sentiment_score.pickle','rb'))
	annot = pickle.load(open('sent_400_wspos.pickle','rb'))

	poscount = bothcount = 0
	posTot = 0
	bothTot = 0
	for line,sent in annot:
		score = (0,0)
		

		string = ''
		for word in line.split():
			string += word.split('#')[0]+' '

		neg = negate.negating(string.strip(' '))

		# catch empty case, simpler than re-pickling
		if neg == []:
			continue

		for i,word in enumerate(line.split()):
			tri = word.split('#')
			if len(tri) == 3:
				pair = (tri[0]+'#'+tri[2],tri[1])
				(a,b) = score
				(c,d) = synDict.get(pair,(0,0))
				tempscore = (a+c,b+d)
			
			if 'NOT' in neg[i]:
				tempscore = (b+d, a+c) # set to reverse value b/c inverted meaning
				
			score = tempscore

			

if __name__ == '__main__':
	svm()