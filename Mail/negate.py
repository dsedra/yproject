#script to negate a POS tagged sentence
import nltk

def negating(line):
	negList = ['dont','cant','wont','not', 'doesnt', 'isnt', 'cannot']
	
	pairs = nltk.pos_tag(line.split())
	words = [] 
	negating = False
	for word,pos in pairs:
		if word in negList:
			negating = True
		elif negating:
			if 'VB' in pos or 'JJ' in pos:
				words.append('NOT' + word)
				continue
			elif 'NN' in pos:
				negating = False
		
		words.append(word)
	return words


if __name__ == '__main__':
	pass
	#f = open('sent_400', 'r')

	#for x in range(100):
	#	line = f.readline()
	#	print line, '------------------------------'
	#	negate(nltk.pos_tag(nltk.word_tokenize(line)))
	#print negating('This app is not good')