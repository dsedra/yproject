yproject
========

Analyzing reviews/comments summer internship project

TO DO:
	- clean up files and add appropriate comments
	- possibly make command line interface for scripts
	- add Makefile possibly if requested


Important files:

1. naive_bayes.py
	- contains all the different classifiers attempted

2. rank.py
	- generate the graph that is used by graph.pl
	- requires a reference file of lines within a class

3. graph.pl
	- runs the PageRank algorithm on a graph
	- graph format is tab separated 'src','dst','edge weight'
	- returns a list of 'node','rank' values  

4. lda.py
	- this file separates the files by topic (currently hardcoded to 3) and returns a graph file and reference list of reviews for each topic.


Overview: This project is a Summer intern project at Yahoo! to attempt to extract meaning from user reviews. The goal was to apply sentiment analysis followed by classification to the reviews in an effort to reduce the amount of time required to understand the important trends in the data. To this end several software packages from diverse sources were used. 



Pre-requistes:
	1. xcode w/ command line tools: https://developer.apple.com/xcode/
	2. Homebrew: http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
	3. Python: http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
	4. NLTK: www.nltk.org
	5. numpy: http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
	6. scipy: http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
	7. gensim: http://radimrehurek.com/gensim/
	
** There may be more packages listed on these websites that need installing!
	 


* n Note that these may have more pre-reqs and should be installed appropriately.
