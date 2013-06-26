import parse, random, codecs

def rand():
	elements = parse.parseFile('ymailh')
	f = codecs.open('gold_sent', 'w', 'utf-8')


	for element in elements:
		if random.random() < 0.1 and len(element.review) > 1:
			f.write(element.review+' &&*%*&& \n')

def more_500():
	elements = parse.parseFile('ymailh')
	f = codecs.open('gold_sent_500','w', 'utf-8')
	for x in range(500):
		f.write(elements[x].review+' &&*%*&& \n')

if __name__ == '__main__':
	more_500()
