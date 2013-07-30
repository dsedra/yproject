import codecs

my = codecs.open('gold_sent_400', 'r', 'utf-8')
his = codecs.open('gold_cross_100', 'r', 'utf-8')


counter = 0

for x in range(100):
	myclass = my.readline().split('&&*%*&&')[1]
	hisclass = my.readline().split('&&*%*&&')[1]

	if 'pos' in myclass and 'pos' in hisclass:
		counter += 1

print counter