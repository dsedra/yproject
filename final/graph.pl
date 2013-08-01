#!/usr/bin/env perl

# contains all the examples in the POD documentation for the module.

use Graph::Centrality::Pagerank;
use Data::Dump qw(dump);
use Data::Dumper;
my $ranker = Graph::Centrality::Pagerank->new();
$listOfEdges = [];

if ($#ARGV+1 < 1){
	print "usage: graph.pl <graph file>\n";
	exit;
}

my $in = $ARGV[0];
my $out = "$ARGV[0]_out";



open(IN,"$in");
open(OUT,">$out");

$count = 0;
while(<IN>){
	chomp;
	($o,$d,$w) = split("\t");
	
	$temp = [];

	$t1 = $o+0;
	$t2 = $d+0;
	$t3 = $w+0;

    #print "Here:[" . $temp[0] . "," . $temp[1] . "]\n";
 	#push @listOfEdges,[$temp[0], $temp[1]];
 	$listOfEdges->[$count] = [$t1, $t2, $t3];
 	$count++;
}

#dump $ranker->getPagerankOfNodes (listOfEdges => $listOfEdges, useEdgeWeights => 1);
#dump $ranker->getPagerankOfNodes (listOfEdges => $new, dampeningFactor => 1);

$hash_ref = $ranker->getPagerankOfNodes (listOfEdges => $listOfEdges,dampeningFactor => 1, linkSinkNodes => 0);



while ( my ($key, $value) = each(%$hash_ref) ) {
        print OUT "$key\t$value\n";
    }






