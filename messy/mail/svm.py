# use score tuple to score reviews in a svm
import parse, pickle, nltk, negate, svmlight

def svm():
	# load the sentiment score file with (word,pos) -> (posScore,negScore) dictionary
	# and the (review,sentiment) pair list
	synDict = pickle.load(open('sentiment_score.pickle','rb'))
	annot = pickle.load(open('sent_400_wspos.pickle','rb'))
	poscount = bothcount = 0
	posTot = 0
	bothTot = 0

	print annot

	# 0 -> pos, 1 -> neg, 2 -> both, 3 -> neut
	data = {'pos':[],'neg':[],'both':[],'neut':[]}
	strToNum = {'pos':0,'neg':1,'both':2,'neut':3}

	for line,sent in annot:
		score = (0,0)
		hits = 0 # number of words found in dictionary, for scaling

		string = ''
		for word in line.split():
			string += word.split('#')[0]+' '

		neg = negate.negating(string.strip(' '))

		# catch empty case, simpler than re-pickling
		if neg == []:
			continue

		# calculate (posScore, negScore) for each word in line
		for i,word in enumerate(line.split()):
			tri = word.split('#')
			tempscore = (0,0)
			if len(tri) == 3:
				hits += 1
				pair = (tri[0]+'#'+tri[2],tri[1])
				tempscore = synDict.get(pair,(0,0))
	
				if 'NOT' in neg[i]:
					tempscore = (tempscore[1],tempscore[0]) # set to reverse value b/c inverted meaning

				
			score = (score[0]+tempscore[0],score[1]+tempscore[1]) # add tempscore to score

		data[sent.strip(' ')].append(score)
		


	featList = []

	# convert to feature lists
	for key in data.keys():
		featList.append(map(lambda (a,b): (strToNum[key],[(1,a),(2,b)]),data[key]))

	

	# construct test and train sets as fractions of featList
	train = featList[0][:3*len(featList[0])/4]+featList[1][:3*len(featList[1])/4]+featList[2][:3*len(featList[2])/4]+featList[3][:3*len(featList[3])/4]
	test = featList[0][3*len(featList[0])/4:]+featList[1][3*len(featList[1])/4:]+featList[2][3*len(featList[2])/4:]+featList[3][3*len(featList[3])/4:]

	for element in train:
		print element

	# train and test model
	model = svmlight.learn(train, type='classification', verbosity=0)
	svmlight.write_model(model, 'my_model1.dat')
	predictions = svmlight.classify(model, test)
	for p in predictions:
		#print '%.8f' % p
		pass	


if __name__ == '__main__':
	#svm()
	temp()