import nltk, parse, re

# POS tags elements then writes them to file
# will read in from file normally for speed 
def pos_tag(filename):
	elements = parse.parseFile(filename)

	tok_sents = [nltk.word_tokenize(element.review) for element in elements]
	for sent in tok_sents:
		for (x,y) in nltk.pos_tag(sent):
			print x,',',y

		print '****'

def processPOS(filename):
	f = open(filename, 'r')

	for line in f.readlines():
		if line != '[]\n':
			singles = line[1:-2].split(',')
			tuples = []
			print singles
			for x in range(0,len(singles),2):
				tuples.append((singles[x],singles[x+1]))
		



if __name__ == '__main__':
	pos_tag('ymailh')