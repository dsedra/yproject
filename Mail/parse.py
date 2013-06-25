# reads in Google reviews for Yahoo! Mail and stores in objects
# creates a list of objects with date, rating, comment, review fields

import re, codecs
def parseFile(filename):
	class Entry:
		def __init__(self, date, rating, comment,review):
			self.date = date
			self.rating = rating
			self.comment = comment
			self.review = review

	# read file in utf-8
	f = codecs.open(filename, 'r', 'utf-8')

	entryList = []

	for line in f.readlines():
		if line == '':
			continue
		list = line.strip().split(" \'")
		if len(list) == 4:
			for x in range(4):
				list[x] = re.sub("<.*>","",list[x]) # remove html remnants
				list[x] = re.sub("\'","",list[x]) # remove single quotes

			splitter = list[0].split(':') # split date and rating apart
			date = list[0].split(':')[0]

			# format rating
			if len(splitter) == 2:
				rating = int(splitter[1].strip(','))
			else:
				continue

			comment = list[2]
			review = list[3]

			newEntry = Entry(date,rating,comment,review)
			entryList.append(newEntry)

	f.close()
	
	return entryList





if __name__ == '__main__':
	parseFile('ymailh')




