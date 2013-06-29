import parse, nltk, codecs

posWords = {'love', 'like', 'good', 'easy', 'functional', 'thanks', 'amazing', 'great', 'best', 'fast', 'excellent'}
negWords = {'bad', 'hate', 'terrible', 'fail', 'worst', 'crash', 'freeze', 'nothing', 'dont', 'cant', 'slow', 'not', 'fix'}
bothWords = {'but', 'however', 'though', 'nevertheless'}

f = codecs.open('gold_sent_400', 'r', 'utf-8')

both = pos = neg = neut = 0


for line in f.readlines():
	pair = line.split('&&*%*&&')
	toks = set(nltk.word_tokenize(pair[0]))
	if (toks&posWords and toks&negWords) or toks&bothWords:
		both += 1
	elif set(nltk.word_tokenize(pair[0]))&negWords:
		neg += 1
	elif set(nltk.word_tokenize(pair[0]))&posWords:
		pos += 1
	else:
		neut += 1

print pos, neg, neut, both




