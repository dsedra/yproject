import parse
from collections import Counter

elements = parse.parseFile('ymailh')

dictionaryList = [{} for x in range(6)]

for element in elements:
	for word in element.review.split():
		dictionaryList[element.rating][word.lower()] = dictionaryList[element.rating].get(word.lower(),0)+1


for i in range(1,6):
	print Counter(dictionaryList[i]).most_common(40)
