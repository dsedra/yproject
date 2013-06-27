import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import parse, codecs, happyfuntokenizing
 
def word_feats(words):
	    return dict([(word, 5) for word in words])

def nb_movierev():
	negids = movie_reviews.fileids('neg')
	posids = movie_reviews.fileids('pos')
	 
	negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
	posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
	 
	trainfeats = negfeats + posfeats
	testfeats = word_feats(my_tok(testStr))


	print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
	 
	classifier = NaiveBayesClassifier.train(trainfeats)
	print classifier.classify(testfeats)
	#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
	#classifier.show_most_informative_features()

def my_tok(string):
	tokens = nltk.word_tokenize(string)
	#tokens = list(set(tokens))
	return tokens

def nb_threeway():
	f = codecs.open('gold_sent_400', 'r', 'utf-8')
	pos = neg = neut = both = 0
	posfeats = negfeats = bothfeats = neutfeats = []
	tok = happyfuntokenizing.Tokenizer(preserve_case=False)

	count = 0
	for line in f.readlines():
		split = line.split('&&*%*&&')
		review = split[0]
		sclass = split[1]

		count += 1

		if 'pos' in sclass:
			posfeats.append( (word_feats(my_tok(line.lower())),'pos') )
			posfeats.append( (word_feats(nltk.util.bigrams(my_tok(line.lower()))),'pos') )
			posfeats.append( (word_feats(nltk.util.ngrams(my_tok(line.lower()),3)),'pos') )
			pos += 1
		elif 'neg' in sclass:
			negfeats.append( (word_feats(my_tok(line.lower())),'neg') )
			negfeats.append( (word_feats(nltk.util.bigrams(my_tok(line.lower()))),'neg') )
			negfeats.append( (word_feats(nltk.util.ngrams(my_tok(line.lower()),3)),'neg') )
			neg += 1
		elif 'neut' in sclass:
			neutfeats.append( (word_feats(my_tok(line.lower())),'neut') )
			neutfeats.append( (word_feats(nltk.util.bigrams(my_tok(line.lower()))),'neut') )
			neutfeats.append( (word_feats(nltk.util.ngrams(my_tok(line.lower()),3)),'neut') )
			neut += 1
		elif 'both' in sclass:
			bothfeats.append( (word_feats(my_tok(line.lower())),'both') )
			bothfeats.append( (word_feats(nltk.util.bigrams(my_tok(line.lower()))),'both') )
			bothfeats.append( (word_feats(nltk.util.ngrams(my_tok(line.lower()),3)),'both') )
			both += 1
		else:
			print 'Unclassified entry on line %d'%(count)
			break
		

	testStr = "I hate the folders in this app!!!!"
	trainfeats = posfeats[:9*pos/10] + negfeats[:9*neg/10] + bothfeats[:9*both/10] + neutfeats[:9*neut/10]
	testfeats = posfeats[9*pos/10:] + negfeats[9*neg/10:] + bothfeats[9*both/10:] + neutfeats[9*neut/10:]
	classifier = NaiveBayesClassifier.train(trainfeats)

	
	classifier.show_most_informative_features()
	print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)

if __name__ == "__main__":
	nb_threeway()

