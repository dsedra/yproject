import nltk.classify.util, pickle, negate, random
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import parse, codecs, happyfuntokenizing, random
from collections import  Counter
from nltk import PorterStemmer 

# derive feature dictionaries from word lists 
# and length param
def word_feats(words):
	posWords = {'love', 'like', 'good', 'easy', 'functional', 'thanks', 'amazing', 'great', 'best', 'fast'}
	negWords = {'bad', 'hate', 'terrible', 'fail', 'worst', 'crash', 'freeze', 'nothing', 'dont', 'cant', 'slow', 'not', 'fix'}
	bothWords = {'but', 'however', 'though', 'nevertheless'}

	feats = dict([(word,'True') for word in words])


	#if (set(words)&bothWords):# or (set(words)&(posWords&negWords)):
	#	feats['bothWord'] = True
	#else:
	#	feats['bothWord'] = False

	#if set(words).intersection(posWords):
	#	feats['posWord'] = True
	#else:
	#	feats['posWord'] = False 

	#if set(words).intersection(negWords):
	#	feats['negWord'] = True
	#else:
	#	feats['negWord'] = False

	return feats


# movie reviews example test
def nb_movierev():
	negids = movie_reviews.fileids('neg')
	posids = movie_reviews.fileids('pos')
	 
	negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
	posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
	 
	trainfeats = negfeats + posfeats
	testfeats = word_feats(my_tok('very good indeed',1))


	print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
	 
	classifier = NaiveBayesClassifier.train(trainfeats)
	print classifier.classify(testfeats)
	#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
	#classifier.show_most_informative_features()

# tokenizer
def my_tok(string, num):
	if num == 1:
		tokens = nltk.word_tokenize(string)
	else:
		tokens = nltk.ngrams(nltk.word_tokenize(string),num)
	
	return tokens

# 
def nb_threeway():
	annot = pickle.load(open('sent_400_wspos_bi.pickle','rb'))

	pos = neg = neut = both = 0
	posfeats = negfeats = bothfeats = neutfeats = []
	tok = happyfuntokenizing.Tokenizer(preserve_case=False)

	count = 0
	lines = []

	for elem in annot:
		review,sclass = elem

		if 'pos' in sclass:
			posfeats.append( (word_feats(my_tok(review.lower(),1)),'pos') )
			posfeats.append( (word_feats(my_tok(review.lower(),2)),'pos') )
			posfeats.append( (word_feats(my_tok(review.lower(),3)),'pos') )
			pos += 1
		elif 'neg' in sclass:
			negfeats.append( (word_feats(my_tok(review.lower(),1)),'neg') )
			negfeats.append( (word_feats(my_tok(review.lower(),2)),'neg') )
			negfeats.append( (word_feats(my_tok(review.lower(),3)),'neg') )
			neg += 1
		#elif 'neut' in sclass:
		#	neutfeats.append( (word_feats(my_tok(review.lower(),1)),'neut') )
			#neutfeats.append( (word_feats(my_tok(review.lower(),2)),'neut') )
			#neutfeats.append( (word_feats(my_tok(line.lower(),3)),'neut') )
		#	neut += 1
		#elif 'both' in sclass:
		#	bothfeats.append( (word_feats(my_tok(review.lower(),1)),'both') )
			#bothfeats.append( (word_feats(my_tok(review.lower(),2)),'both') )
			#bothfeats.append( (word_feats(my_tok(review.lower(),3)),'both') )
		#	both += 1
		else:
			print 'Unclassified entry on line %d'%(count)
			break

	
	testStr = "i like this app and hate this app!!!!"
	trainfeats = posfeats[:9*pos/10] + negfeats[:9*neg/10] + bothfeats[:9*both/10] + neutfeats[:9*neut/10]
	#testfeats = posfeats[9*pos/10:] + negfeats[9*neg/10:] + bothfeats[9*both/10:] + neutfeats[9*neut/10:]
	classifier = NaiveBayesClassifier.train(trainfeats)

	#match = 0
	matchCountDict = {}
	countDict = {}
	for elem in annot:
		review,sclass = elem

		testfeats = {}
		testfeats = word_feats(my_tok(review.lower(),1))
		#testfeats.update(word_feats(my_tok(review.lower(),2)))
		#testfeats.update(word_feats(my_tok(review.lower(),3)))

		choice = classifier.classify(testfeats)

		#print review, choice
		if  choice in sclass:
			matchCountDict[choice] = matchCountDict.get(choice,0)+1
			#print line

		countDict[choice] = countDict.get(choice,0)+1
		

	print matchCountDict
	print countDict
	print pos,neg

	classifier.show_most_informative_features()
	#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
	#print classifier.classify(word_feats(my_tok(testStr)))



# Naive Bayes attempt to classify based on two features 
def nb_bi():
	synDict = pickle.load(open('sentiment_score.pickle','rb'))
	annot = pickle.load(open('sent_400_wspos_bi.pickle','rb'))
	stopList = ['and','the','or','of','is']

	random.shuffle(annot)
	annot.remove(('#NR \n','pos \n'))

	posNum = negNum = posaNum = negaNum = 0
	posfeats = []
	negfeats = []
	scores = []

	for line,sent in annot:
		score = (0,0)

		string = ''
		words = []

		for word in line.strip().split():
			words.append(word.split('#')[0])

		string = ' '.join(words)


		neg = negate.negating(string.strip(' '))

		(p,n) = score

		# construct features dictionary
		feats = {} #{'pos':p, 'neg':n}
		for word in words:
			if word not in stopList:
				feats[word] = True
		scores.append(feats)

	
		

		# try simple analytics
		if 'pos' in sent:
			posfeats.append((feats,'pos'))
		elif 'neg' in sent:
			negfeats.append((feats,'neg'))
		
		if ( p >= n+0.05 or score == (0,0) ) and 'pos' in sent:
			posNum += 1
		elif p < n+0.05 and 'neg' in sent:
			negNum += 1

		if 'pos' in sent:
			posaNum += 1
		elif 'neg' in sent:
			negaNum +=1 
		else:
			print 'massive prob!!'

		if p >= n and 'neg' in sent:
			#print line, ' pos, neg', score
			pass
		elif p < n and 'pos' in sent:
			#print line, ' neg, pos', score
			pass

	# test Naive Bayes

	lenPos = 5*len(posfeats)/12
	lenNeg = 5*len(negfeats)/12


	classifier = NaiveBayesClassifier.train(posfeats[:lenPos]+negfeats[:lenNeg])
	print nltk.classify.util.accuracy(classifier, posfeats[lenPos:]+negfeats[lenNeg:])


	count = total = 0
	for i,(line,sent) in enumerate(annot):
		if sent.strip(' \n') in classifier.classify(scores[i]).strip(' \n'):
			count += 1 
	
		total += 1

	print count,total 
				
	#print 'claim: ',posNum,' ',negNum
	#print 'actual: ',posaNum,' ',negaNum

def nb_vector():
	annot = pickle.load(open('sent_400_wspos_bi.pickle','rb'))
	synDict = pickle.load(open('sentiment_score.pickle','rb'))

	random.shuffle(annot)

	length = 3*len(annot)/4
	train = annot[:length]
	test = annot[length:]

	posDict = {}
	negDict = {}
	npos = nneg = 0

	for line,sent in train:
		for wordTag in line.strip().split(' '):
			word = wordTag.split('#')[0]

			if 'pos' in sent:
				npos += 1
				posDict[word] = posDict.get(word,0) + 1
			else:
				nneg += 1
				negDict[word] = negDict.get(word,0) + 1

	print posDict

	classifier = NaiveBayesClassifier.train([(posDict,'pos'),(negDict,'neg')])


	correct = pos = 0

	for line,sent in test:
		wordDict = {}

		for wordTag in line.lower().split(' '):
			word = wordTag.split('#')[0]
			wordDict[word] = wordDict.get(word,0) + 1

		res = classifier.classify(wordDict)
		if res == 'neg' and res not in sent:
			pneg = classifier.prob_classify(wordDict).prob('neg')
			print pneg, 1-pneg



## uses constructFeats to build feature vectors	
def calcScoreVec():
	dic = pickle.load(open('sentiment_ranking.pickle','rb'))
	synDict = pickle.load(open('sentiment_score.pickle','rb'))

	annotPlain = pickle.load(open('sent_400_bi.pickle','rb'))
	annotFancy = pickle.load(open('sent_400_wspos_bi.pickle','rb'))
	pairList = []

	for i,x in enumerate(annotPlain):
		pairList.append((x,annotFancy[i]))


	random.shuffle(pairList)

	lenTrain = 5*len(pairList)/6
	train = pairList[:lenTrain]
	test = pairList[lenTrain:]

	# ---------------- begin first classifier --------------- #

	training1 = []
	testing1 = []

	for pair in train:
		line,sent = pair[0]
		training1.append(constructFeats(line,sent,dic))



	# --------------- begin second classifier -------------- #

	training2 = []
	testing2 = []

	for pair in train:
		line,sent = pair[1]
		training2.append(constructFeats2(line,sent,synDict))


	# --------------- begin selection classifier ----------- #
	training3 = constructFeats3(pairList,train)
	testing3 = constructFeats3(pairList,test)
	
	classifier3 = NaiveBayesClassifier.train(training3)

	print 'accuracy:', nltk.classify.util.accuracy(classifier3, testing3)
	# --------------- compile stats ---------------- #

	#classifier2 = NaiveBayesClassifier.train(training2)
	#classifier1 = NaiveBayesClassifier.train(training1)
	#classifier3 = NaiveBayesClassifier.train(training3)


	#statsList = []
	
	#for pair in test:
	#	line0,sent0 = pair[0]
	#	line1,sent1 = pair[1]

	#	feats1 = constructFeats(line0,sent0,dic)
	#	feats2 = constructFeats2(line1,sent1.strip(),synDict)

		#feats[0].update(constructFeats2(pair[1][0],sent,synDict))
	#	feats3 = constructFeats3(pairList,test)	
	#	ppos1 = classifier1.prob_classify(feats1[0]).prob('pos')
	#	clas1 = classifier1.classify(feats1[0])

	#	ppos2 = classifier2.prob_classify(feats2[0]).prob('pos\n')
	#	clas2 = classifier2.classify(feats2[0])

		
	#	statsList.append((sent0,clas1,clas2.strip(),ppos1,ppos2))

	#twoStats(statsList)



# work with most informative ?? features
def constructFeats3(pairList,whichever):
	from nltk.probability import FreqDist, ConditionalFreqDist
	from nltk.metrics import BigramAssocMeasures


	word_fd = FreqDist()
	label_word_fd = ConditionalFreqDist()

	for pair in pairList:
		line,sent = pair[0]
		for word in nltk.word_tokenize(line):
			word_fd.inc(word.lower())
			label_word_fd[sent].inc(word.lower())

	pos_word_count = label_word_fd['pos'].N()
	neg_word_count = label_word_fd['neg'].N()
	total_word_count = pos_word_count + neg_word_count


	word_scores = {}
	for word, freq in word_fd.iteritems():
		pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word],(freq, pos_word_count),total_word_count)
		neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word],(freq, neg_word_count),total_word_count)
		word_scores[word] = pos_score + neg_score
 
	best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:18]
	bestwords = set([w for w, s in best])
	
	training3 = []
	testing3 = []

	for pair in whichever:
		line,sent = pair[0]
		training3.append((best_word_feats(nltk.word_tokenize(line.lower()),bestwords),sent))

	return training3

def best_word_feats(words,bestwords):
    return dict([(word, True) for word in words if word in bestwords])

# construct feats from SentiWordNet dict
def constructFeats2(line,sent,synDict):
	feats = {}
	score = (0,0)

	words = []
	for word in line.strip().split(' '):
		words.append(word.split('#')[0])

	neg = negate.negating(' '.join(words))


	for i,word in enumerate(line.strip().split(' ')):
		parts = word.split('#')

		if len(parts) == 3:
			#feats[parts[0]] = synDict.get((parts[0]+'#'+parts[2],parts[1]),(0,0))
		 	a,b = synDict.get((parts[0]+'#'+parts[2],parts[1]),(0,0))

		 	if 'NOT' in neg[i]:
		 		score = (score[0]+b,score[1]+a)
		 	else:
		 		score = (score[0]+a,score[1]+b)

		
	feats['ps'] = score[0]
	feats['ns'] = score[1]

	return (feats,sent)

# construct feats for subj clues dict
def constructFeats(line,sent,dic):
	feats = {}
	mapping = {('weaksubj','positive'):1,('strongsubj','positive'):2,('weaksubj','negative'):-1,('strongsubj','negative'):-2}
	sumscore = 0

	for word,pos in nltk.pos_tag(nltk.word_tokenize(line.lower())):
		score = None

		if 'NN' in pos:
			score = lookup(dic,word,'noun')
		elif 'JJ' in pos:
			score = lookup(dic,word,'adj')
		elif 'VB' in pos:
			score = lookup(dic,word,'verb')
		elif 'RB' in pos:
			score = lookup(dic,word,'adverb')

		if score:
			(e1,e2,e3) = score
			val = mapping.get((e2,e1),0)
			feats[word] = val

			sumscore += val

			
	feats['sum'] = sumscore

	
	return (feats,sent)	

	
# takes sent,clas1,clas2,ppos1,ppos2
def twoStats(tuples):

	statsList = []

	for ele in tuples:
		sent,c1,c2,p1,p2 = ele
		best = ''

		if mostConf(c1,p1) > mostConf(c2,p2):
			statsList.append((sent,c1,p1,1-p1))
		else:
			statsList.append((sent,c2,p2,1-p2))

	stats(statsList)
		

def mostConf(sent,ppos):
	if 'pos' in sent:
		return ppos
	else:
		return 1-ppos


# takes sent,class,ppos,pneg for one classifier
def stats(tuples):
	accuracy = pos = neg = posc = negc = 0
	for ele in tuples:
		if ele[0] in ele[1]:
			accuracy += 1
		if 'pos' in ele[0]:
			pos += 1
			if 'pos' in ele[1]:
				posc += 1
		if 'neg' in ele[0]:
			neg += 1
			if 'neg' in ele[1]:
				negc += 1
	print len(tuples),'\t',posc,pos,'\t',negc,neg,'\t',accuracy




def lookup(dict,word,pos):
	if (word,pos) in dict:
		return dict[(word,pos)]
	elif (word,'anypos') in dict:
		return dict[(word,'anypos')]
	elif (word,'adj') in dict:
		return dict[(word,'adj')]
	elif (word,'noun') in dict:
		return dict[(word,'noun')]
	elif (word,'verb') in dict:
		return dict[(word,'verb')]
	elif (word,'adverb') in dict:
		return dict[(word,'adverb')]


if __name__ == "__main__":
	#nb_bi()
	#nb_vector()
	calcScoreVec()


