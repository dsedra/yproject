# naive Baise classifier for ratings

import parse, random, math
from nltk import bigrams

# parse raw file into object list
entryList = parse.parseFile('ymailh')

def test():
	uniDictList = [{} for x in range(6)]
	biDictList = [{} for x in range(6)]
	vocabSize = [0 for x in range(6)]
	totalSize = [0 for x in range(6)]
	biVocabSize = [0 for x in range(6)]
	bitotalSize = [0 for x in range(6)]
	numList = [0 for x in range(6)]
	numCorrect = total = 0

	# randomly split set 
	for entry in entryList:
		if random.random() > 0.10:
			entry.test = 0
		else:
			entry.test = 1

	# compute train dictionaries
	for entry in entryList:
		if entry.test == 0:
			for word in entry.review.split():
				uniDictList[entry.rating][word] = uniDictList[entry.rating].get(word,0)+1 

			for bigram in bigrams(entry.review.split()):
				biDictList[entry.rating][bigram] = biDictList[entry.rating].get(word,0)+1
							 
			numList[entry.rating] += 1


	print numList

	totalCount = reduce(lambda x,y: x+y, numList)


	# compute dictionary stats
	for x in xrange(1,6):
		vocabSize[x] = len(uniDictList[x].keys())
		totalSize[x] = reduce(lambda x,y: x+y,uniDictList[x].values())
		biVocabSize[x] = len(biDictList[x].keys())
		bitotalSize[x] = reduce(lambda x,y: x+y,biDictList[x].values())
			
	# testing
	for entry in entryList:
		if entry.test == 1:
			rankProb = [0 for x in range(6)]
			for x in range(1,6):
				for word in entry.review.split():
					#rankProb[x] += math.log(uniDictList[x].get(word,1)) - math.log(vocabSize[x]+totalSize[x])
					pass
				for bigram in bigrams(entry.review.split()):
					rankProb[x] += math.log(biDictList[x].get(bigram,1)) - math.log(biVocabSize[x]+bitotalSize[x])

			map(lambda x: x*numList[entry.rating]/totalCount,rankProb)
			entry.pRating = rankProb.index(max(rankProb[1:6]))
			if entry.pRating == entry.rating:
				numCorrect += 1
			total += 1
		print bigrams(entry.review.split())


	return [numCorrect, total]

def main():
	print test()

main()