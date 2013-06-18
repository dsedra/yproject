# naive Baise classifier for ratings

import parse, random, math

# parse raw file into object list
entryList = parse.parseFile('ymailh')

def test():
	dictionaryList = [{} for x in range(6)]
	vocabSize = [0 for x in range(6)]
	totalSize = [0 for x in range(6)]
	numList = [0 for x in range(6)]
	numCorrect = total = 0

	# randomly split set 
	for entry in entryList:
		if random.random() > 0.7:
			entry.test = 0
		else:
			entry.test = 1

	# compute train dictionaries
	for entry in entryList:
		if entry.test == 0:
			for word in entry.review.split():
				dictionaryList[entry.rating][word] = dictionaryList[entry.rating].get(word,0)+1 
			numList[entry.rating] += 1

	totalCount = reduce(lambda x,y: x+y, numList)


	# compute dictionary stats
	for x in xrange(1,6):
		vocabSize[x] = len(dictionaryList[x].keys())
		totalSize[x] = reduce(lambda x,y: x+y,dictionaryList[x].values())
			
	# testing
	for entry in entryList:
		if entry.test == 1:
			rankProb = [0 for x in range(6)]
			for x in range(1,6):
				for word in entry.review.split():
					rankProb[x] += math.log(dictionaryList[x].get(word,1)) - math.log(vocabSize[x]+totalSize[x])
			map(lambda x: x*numList[entry.rating]/totalCount,rankProb)
			entry.pRating = rankProb.index(max(rankProb[1:6]))
			if entry.pRating == entry.rating:
				numCorrect += 1
			total += 1


	return [numCorrect, total]

def main():
	sum = 0
	for i in range(100):
		pair = test()
		sum += float(pair[0])/pair[1]

	print sum/100
main()