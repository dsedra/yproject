#read in SentiWordnet 3.0

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

for line in f.readlines():
	splits = line.split('\t')

	syns = []
	for ele in splits[4].split():
		syns.append(ele.split('#')[0])
	
	newSyn = Syn(splits[0],splits[1],splits[2],splits[3],syns,splits[5])
	synList.append(newSyn)


for syn in synList:
	for ele in syn.syns:
		if ele == 'hate':
			print syn.posScore,syn.negScore