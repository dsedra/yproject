import parse, nltk, codecs


def wordCount():
	wordDict ={}

	for line in open('gold_sent_400_bi','r').readlines():
		for word in line.split(' &&*%*&& ')[0].lower().split(' '):
			wordDict[word] = wordDict.get(word,0) + 1

	print wordDict

def test():
	from semanticpy.vector_space import VectorSpace

	vector_space = VectorSpace(["The cat in the hat disabled", "A cat is a fine pet ponies.", "Dogs and cats make good pets.","I haven't got a hat."])

	#Search for cat
	print vector_space.search(["cat"])

	#Show score for relatedness against document 0
	print vector_space.related(0)

if __name__ == '__main__':
	test()





