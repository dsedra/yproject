"""

Master file which incorporates polarity classification, topic modeling, and ranking.

"""

import pickle
import sys
import getopt
import os

# classifier
import nltk
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.classify import NaiveBayesClassifier

# lda
import pickle, nltk, gensim, logging
from gensim import corpora, models, similarities
from operator import itemgetter
import subprocess
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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



	# read in both the training file and the test file (the one we actually) want to classify
	trainLines = [tuple(line.strip('\n').split(' &&*%*&& ')) for line in trainf.readlines()]
	testLines = [line.strip() for line in testf.readlines()]

	bestwords = get_best_words(trainLines, num_best_words)
	
	classifier = build_classifier(trainLines,bestwords)

	# classify entire test set
	classified = classify(testLines,bestwords,classifier)

	# generate positive and negative models
	neg_lda = generate_model(classified['neg'],topics)
	#pos_lda = generate_model(classified['pos'],topics)

	neg_bins = get_bins(classified['neg'],neg_lda,topics)
	#pos_bins = get_bins(classified['pos'],pos_lda,topics):
	
	generate_graph(neg_bins,'neg')
	#generate_graph(pos_bins,'pos')

	get_top(neg_bins,'neg',num_top)

# return the top reviews from each topic using
# output of generate_graph 
def get_top(bins, prefix, num_top):
	for i,bin in enumerate(bins):
		name = prefix + '_' + str(i) + '_out'
		cf = open(name,'r')

		scores = []
		for line in cf.readlines():
			pair = line.strip().split('\t')
			num,score = int(pair[0]),float(pair[1])
			scores.append((num,score))

		print 'bin no. ',i
		for ele in bin:
			print ele



		srt = sorted(scores,key=itemgetter(1),reverse=True)
		print 'prefix',i,map(lambda x: x[0],srt[:num_top]),len(bin)


def get_bins(lines, lda, num_bins):
	corpus,dictionary = generate_corpus(lines)
	bins = [[] for x in xrange(num_bins)]

	doc_lda = lda[corpus]

	for i,ele in enumerate(doc_lda):
		index,score = max(ele,key=itemgetter(1))
		bins[index].append(lines[i])
	
	return bins

def generate_corpus(lines):
	# create corpus
	wordLists = []
	stopwords = {'and','or','for','a','of','it','app', 'the'}

	wordLists = [[word for word in nltk.word_tokenize(doc.lower()) if word not in stopwords] for doc in lines]

	vocab = sum(wordLists, [])
	
	singles = set(word for word in set(vocab) if vocab.count(word) == 1)

	wordLists = [[word for word in text if word not in singles] for text in wordLists]
	dictionary = corpora.Dictionary(wordLists)

	corpus = [dictionary.doc2bow(text) for text in wordLists]

	return (corpus,dictionary)

# lda stuff
def generate_model(lines, num_topics):
	# create corpus
	corpus,dictionary = generate_corpus(lines)

	# generate model

	tfidf = models.TfidfModel(corpus)

	corpora.MmCorpus.serialize('corpus.mm', corpus)

	corpus = corpora.MmCorpus('corpus.mm')

	tfidf = models.TfidfModel(corpus)

	corpus_tfidf = tfidf[corpus]
	
	lda = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics, update_every=0, chunksize=5, passes=20)
	lda.show_topic(topicid=0, topn=num_topics)
	
	return lda

# takes lines and outputfile prefix (e.g. positive) and 
# generates graph files for each of the 
def generate_graph(bins, prefix):
	for k,bin in enumerate(bins):
		fname = prefix + '_' + str(k)
		cf = open(fname, 'w')

		print len(bin),'##$$$'

		for i,line1 in enumerate(bin):
			print i
			for j,line2 in enumerate(bin):
				intersect = len(set(nltk.word_tokenize(line1)) & set(nltk.word_tokenize(line2)))
				if i != j and intersect > 0:
					out = '\t'.join([str(i),str(j),str(intersect)])+'\n'
					cf.write(out)

		# run PageRank script on generated graph, then delete temp graph file
		subprocess.call(['perl','graph.pl',fname])
		cf.close()
		#os.remove(fname)

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

