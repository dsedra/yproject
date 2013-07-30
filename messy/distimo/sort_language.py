# sort out all non-English comments
import codecs, sys, errno;


def cleanNonAscii():
	filename = 'newtest.csv'

	f = codecs.open(filename, 'r', 'utf-8',errors='strict')
	
	eList = []

	for line in f.readlines():
		newEntry = Entry()
		newEntry.date = line.split(',')[0]
		newEntry.store = line.split(',')[1]
		newEntry.app = line.split(',')[2]
		newEntry.comment = line.split(',')[5]
		newEntry.review = line.split(',')[6]
		newEntry.user = line.split(',',)[7]
		newEntry.rating = line.split(',')[9]

		eList.append(newEntry)


class Entry:
	pass
		
# find the nth char in direction {l,r}
def findNth(str, charIn, direction, n):
	if len(str) == 0 or (direction != 'r' and direction != 'l'):
		return -1

	if direction == 'l':
		count = 0
		for x in range(len(str)):
			if str[x] == charIn:
				count += 1
			if count == n:
				return x
		return -1

	if direction == 'r':
		count = 0
		for x in range(len(str)):
			



cleanNonAscii()