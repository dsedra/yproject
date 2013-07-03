# read in SentiWordnet 3.0 and create a dictionary from 
# (word,pos) -> (posScore,negScore) which is then pickled
import pickle

f = open('sw3.txt', 'r')

class Syn:
	def __init__(self,pos,num,posScore,negScore,syns,meaning):
		self.pos = pos
		self.num = num
		self.posScore = posScore
		self.negScore = negScore
		self.meaning = meaning
		self.syns = syns

synList = []
synDict = {}
revList = []

for line in f.readlines():
	splits = line.split('\t')

	syns = []
	for ele in splits[4].split():
		syns.append(ele.split('#')[0])

	for syn in syns:
		(a,b) = synDict.get((syn,splits[0]),(0,0))
		synDict[(syn,splits[0])] = (a+float(splits[2]),b+float(splits[3]))
	


for key in synDict.keys():
	if synDict[key] == (0,0):
		synDict.pop(key)


pickle.dump(synDict, open('sentiment_score.pickle', 'wb'))



f.close()
r.close()

