#!/usr/bin/perl

use Graph::Centrality::Pagerank;
use Data::Dump qw(dump);
my $ranker = Graph::Centrality::Pagerank->new();
my $listOfEdges = [[1,2],[2,3]];
open(FILE,'graph');

while(<FILE>){
	chomp;
	($o,$d,$w) = split("\t");
}
#ump $ranker->getPagerankOfNodes (listOfEdges => $listOfEdges, dampeningFactor => 1);