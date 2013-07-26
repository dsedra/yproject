use Graph::Centrality::Pagerank;
use Data::Dump qw(dump);
my $ranker = Graph::Centrality::Pagerank->new();
my $listOfEdges = [[1,3],[1,2],[2,4],[3,2],[3,5],[4,2],[4,5],[4,6],[5,6],[5,7],[5,8],[6,8],[7,5],[7,8],[8,6],[8,7]];
dump $ranker->getPagerankOfNodes (listOfEdges => $listOfEdges,dampeningFactor => 1, linkSinkNodes => 0);