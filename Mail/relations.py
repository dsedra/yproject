import nltk, parse

elements = parse.parseFile('ymailh')

tok_sents = [nltk.word_tokenize(element.review) for element in elements]
for sent in tok_sents:
	print nltk.pos_tag(sent)

