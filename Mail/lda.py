import pickle, nltk, gensim, logging
from gensim import corpora, models, similarities
from operator import itemgetter

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def lda_first(corpus):
	tfidf = models.TfidfModel(corpus)

	corpora.MmCorpus.serialize('corpus.mm', corpus)

	corpus = corpora.MmCorpus('corpus.mm')

	tfidf = models.TfidfModel(corpus)

	corpus_tfidf = tfidf[corpus]

	#lsi = models.LsiModel(corpus_tfidf, id2word=id2word, num_topics=3) # initialize an LSI transformation
	#corpus_lsi = lsi[corpus_tfidf]
	#lsi.print_topics(3)

	
	lda = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=3, update_every=0, chunksize=10, passes=20)
	lda.show_topic(topicid=0, topn=3)
	
	return lda

def test_lda(corpus,posDocs):
	lda = lda_first(corpus)

	doc_lda = lda[corpus]

	# number of topics
	bins = [[],[],[]]

	for i,ele in enumerate(doc_lda):
		
		index,score = max(ele,key=itemgetter(1))
		bins[index].append(posDocs[i])
	
	for bin in bins:
		print '\n\n'
		for item in bin:
			print item
		print '\n\n'

if __name__ == '__main__':
	annotPlain = pickle.load(open('sent_400_bi.pickle','rb'))
	posDocs = []
	wordLists = []
	stopwords = {'and','or','for','a','of','it','app', 'the'}

	for line,sent in annotPlain:
		if sent == 'pos':
			posDocs.append(line)

	total = 0
	for rev in posDocs:
		total += len(nltk.word_tokenize(rev))

	print total,len(posDocs)

	wordLists = [[word for word in nltk.word_tokenize(doc.lower()) if word not in stopwords] for doc in posDocs]

	vocab = sum(wordLists, [])
	
	singles = set(word for word in set(vocab) if vocab.count(word) == 1)

	wordLists = [[word for word in text if word not in singles] for text in wordLists]
	dictionary = corpora.Dictionary(wordLists)

	dictionary.save_as_text('dict.txt')

	id2word = gensim.corpora.Dictionary.load_from_text('dict.txt')

	corpus = [dictionary.doc2bow(text) for text in wordLists]

	#test_lda(corpus,posDocs)