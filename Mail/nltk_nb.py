import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import parse, codecs
 
def word_feats(words):
	    return dict([(word, True) for word in words])

def nb_movierev():
	negids = movie_reviews.fileids('neg')
	posids = movie_reviews.fileids('pos')
	 
	negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
	posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

	 
	#negcutoff = len(negfeats)*3/4
	#poscutoff = len(posfeats)*3/4
	 
	trainfeats = negfeats + posfeats



	testStr = "I love the app."
	testfeats = word_feats(nltk.word_tokenize(testStr))


	print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
	 
	classifier = NaiveBayesClassifier.train(trainfeats)
	print classifier.classify(testfeats)
	#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
	#classifier.show_most_informative_features()


def nb_threeway():
	f = codecs.open('gold_sent', 'r', 'utf-8')
	pos = neg = neut = both = 0
	posfeats = negfeats = bothfeats = neutfeats = []

	for line in f.readlines():
		split = line.split('&&*%*&&')
		review = split[0]
		sclass = split[1]

		if 'pos' in sclass:
			posfeats.append( (word_feats(nltk.word_tokenize(line)),'pos') )
		elif 'neg' in sclass:
			negfeats.append( (word_feats(nltk.word_tokenize(line)),'neg') )
		elif 'neut' in sclass:
			neutfeats.append( (word_feats(nltk.word_tokenize(line)),'neut') )
		elif 'both' in sclass:
			bothfeats.append( (word_feats(nltk.word_tokenize(line)),'both') )
		else:
			print 'aaaaa!!!'
			break


	testStr = "I love the new layout and design. It is much better than the previous app!!"
	trainfeats = posfeats + negfeats + bothfeats + neutfeats
	testfeats = word_feats(nltk.word_tokenize(testStr))
	classifier = NaiveBayesClassifier.train(trainfeats)

	print classifier.classify(testfeats)
	#classifier.show_most_informative_features()
	#print 'accuracy:', nltk.classify.util.accuracy(classifier, trainfeats)

if __name__ == "__main__":
	nb_threeway()