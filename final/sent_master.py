"""

Master file which incorporates polarity classification, topic modeling, and ranking.

"""

import pickle
import sys
import getopt

#classifier
import nltk
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.classify import NaiveBayesClassifier

def main(argv):
	# params
	num_best_words = 18

	try:
		opts, args = getopt.getopt(argv, 'a:s:t:n:')
	except getopt.GetoptError:
		print 'usage: -a <annotated file> -s <test file> -t <number of topics> -n <number per topic>'
		sys.exit(2)

	trainf = ''
	testf = ''
	topics = num_top = 3

	for opt, arg in opts:
		if opt == '-a':
			try:
				trainf = open(arg, 'rb')
			except IOError:
				print "Couldn't find annotated file"
				exit()
		elif opt == '-s':
			try:
				testf = open(arg, 'rb')
			except IOError:
				print "Couldn't find test file"
				exit()
		elif opt == '-t':
			arg = int(arg)
			if opt <= 0:
				print "Non-negative no. topics, please"
				exit(0)
			else:
				topics = arg
		elif opt == '-n':
			arg = int(arg)
			if opt <= 0:
				print "Non-negative no. topics, please"
				exit(0)
			else:
				num_top = arg

	# read in both the training file
	# and the test file (the one we actually)
	# want to classify
	trainLines = [tuple(line.strip('\n').split(' &&*%*&& ')) for line in trainf.readlines()]
	testLines = [line.strip() for line in testf.readlines()]

	bestwords = get_best_words(trainLines, num_best_words)
	
	classifier = build_classifier(trainLines,bestwords)

	# classify entire test set
	classified = classify(testLines,bestwords,classifier)

	# generate two output graphs 
	generate_graph(classified)

	
def generate_graph(classified):
	p_file = open('graph_pos', 'w')
	n_file = open ('graph_neg', 'w')

	print 'asdfadfasd'

	print len(classified['pos']),len(classified['neg'])
	
	for i,line1 in enumerate(classified['pos']):
		for j,line2 in enumerate(classified['pos']):
			intersect = len(set(nltk.word_tokenize(line1)) & set(nltk.word_tokenize(line2)))
			if i != j and intersect > 0:
				out = '\t'.join([str(i),str(j),str(intersect)])+'\n'
				p_file.write(out)

	for i,line1 in enumerate(classified['neg']):
		for j,line2 in enumerate(classified['neg']):
			intersect = len(set(nltk.word_tokenize(line1)) & set(nltk.word_tokenize(line2)))
			if i != j and intersect > 0:
				out = '\t'.join([str(i),str(j),str(intersect)])+'\n'
				n_file.write(out)





def build_classifier(lines, bestwords):
	trainFeats = []
	for line,sent in lines:
		locDict = {}
		for word in nltk.word_tokenize(line.lower()):
			if word in bestwords:
				locDict[word] = True
		trainFeats.append((locDict,sent.strip(' ')))

	return NaiveBayesClassifier.train(trainFeats)

def classify(testLines,bestwords,classifier):
	classes = {'pos':[],'neg':[]}

	for line in testLines:
		locDict = {}
		for word in nltk.word_tokenize(line.lower()):
			if word in bestwords:
				locDict[word] = True

		classes[classifier.classify(locDict)].append(line)

	return classes

# takes a list of (word,sentiment) pairs
def get_best_words(words_list, num_best_words):
	from nltk.probability import FreqDist, ConditionalFreqDist
	from nltk.metrics import BigramAssocMeasures


	word_fd = FreqDist()
	label_word_fd = ConditionalFreqDist()

	for pair in words_list:
		line,sent = pair
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
 
	best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:num_best_words]
	bestwords = set([w for w, s in best])

	return bestwords

def best_bigram_word_feats(words, bestwords, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    d = dict([(bigram, True) for bigram in bigrams])
    d.update(best_word_feats(words,bestwords))
    return d

def best_word_feats(words,bestwords):
    return dict([(word, True) for word in words if word in bestwords])

if __name__ == '__main__':
	main(sys.argv[1:])

