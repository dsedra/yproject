import nltk.classify.util, pickle, negate, random
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import parse, codecs, happyfuntokenizing, random
from collections import  Counter
 

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



		
def calcScoreVec():
	dic = {}
	for line in open('subjclueslen1.tff','r').readlines():
		lists = line.split()
		newList = []

		for ele in lists:
			newList.append(ele.split('=')[1])

		
		dic[newList[2],newList[3]] = (newList[5],newList[0],newList[4])
	print dic
	
	
if __name__ == "__main__":
	#nb_bi()
	#nb_vector()
	calcScoreVec()


