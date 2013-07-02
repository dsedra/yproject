import nltk.classify.util
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

	feats = {} #dict([(word,'True') for word in words])


	if (set(words)&bothWords):# or (set(words)&(posWords&negWords)):
		feats['bothWord'] = True
	else:
		feats['bothWord'] = False

	if set(words).intersection(posWords):
		feats['posWord'] = True
	else:
		feats['posWord'] = False 

	if set(words).intersection(negWords):
		feats['negWord'] = True
	else:
		feats['negWord'] = False

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
	f = codecs.open('gold_sent_400', 'r', 'utf-8')
	pos = neg = neut = both = 0
	posfeats = negfeats = bothfeats = neutfeats = []
	tok = happyfuntokenizing.Tokenizer(preserve_case=False)

	count = 0
	lines = []

	for line in f.readlines():
		split = line.split('&&*%*&&')
		review = split[0]
		sclass = split[1]
		lines.append(line)
		count += 1

		if 'pos' in sclass:
			posfeats.append( (word_feats(my_tok(review.lower(),1)),'pos') )
			#posfeats.append( (word_feats(my_tok(review.lower(),2)),'pos') )
			#posfeats.append( (word_feats(my_tok(review.lower(),3)),'pos') )
			pos += 1
		elif 'neg' in sclass:
			negfeats.append( (word_feats(my_tok(review.lower(),1)),'neg') )
			#negfeats.append( (word_feats(my_tok(review.lower(),2)),'neg') )
			#negfeats.append( (word_feats(my_tok(review.lower(),3)),'neg') )
			neg += 1
		elif 'neut' in sclass:
			neutfeats.append( (word_feats(my_tok(review.lower(),1)),'neut') )
			#neutfeats.append( (word_feats(my_tok(review.lower(),2)),'neut') )
			#neutfeats.append( (word_feats(my_tok(line.lower(),3)),'neut') )
			neut += 1
		elif 'both' in sclass:
			bothfeats.append( (word_feats(my_tok(review.lower(),1)),'both') )
			#bothfeats.append( (word_feats(my_tok(review.lower(),2)),'both') )
			#bothfeats.append( (word_feats(my_tok(review.lower(),3)),'both') )
			both += 1
		else:
			print 'Unclassified entry on line %d'%(count)
			break

	print bothfeats
	testStr = "i like this app and hate this app!!!!"
	trainfeats = posfeats[:9*pos/10] + negfeats[:9*neg/10] + bothfeats[:9*both/10] + neutfeats[:9*neut/10]
	#testfeats = posfeats[9*pos/10:] + negfeats[9*neg/10:] + bothfeats[9*both/10:] + neutfeats[9*neut/10:]
	classifier = NaiveBayesClassifier.train(trainfeats)

	#match = 0
	matchCountDict = {}
	countDict = {}
	for line in lines:
		split = line.split('&&*%*&&')
		review = split[0]
		sclass = split[1]

		testfeats = {}
		testfeats = word_feats(my_tok(review.lower(),1))
		#testfeats.update(word_feats(my_tok(review.lower(),2)))
		#testfeats.update(word_feats(my_tok(review.lower(),3)))

		choice = classifier.classify(testfeats)

		print review, choice
		if  choice in sclass:
			matchCountDict[choice] = matchCountDict.get(choice,0)+1
			#print line

		countDict[choice] = countDict.get(choice,0)+1
		

	print matchCountDict
	print countDict
	print both,pos,neg,neut

	classifier.show_most_informative_features()
	#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
	#print classifier.classify(word_feats(my_tok(testStr)))


if __name__ == "__main__":
	nb_threeway()


