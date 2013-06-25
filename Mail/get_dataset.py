import parse, random, codecs

elements = parse.parseFile('ymailh')
f = codecs.open('gold_sent', 'w', 'utf-8')


for element in elements:
	if random.random() < 0.1 and len(element.review) > 1:
		f.write(element.review+' &&*%*&& \n')
		

