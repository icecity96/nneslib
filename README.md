# NNESLIB
nneslib is a python library for evaluating Network Nodes or Edges Significance (NNES). 
This Library is written in pure Python and based on Networkx.

> nneslib is forced to undirected graph. Directed graph may be considered in next version of

[TOC]

## Implemented Methods
### Node
### Edge
1. betweenness_centrality: \[weighted | unweighted\]
    1. [A Faster Algorithm for Betweenness Centrality. Ulrik Brandes, Journal of Mathematical Sociology 25(2):163-177, 2001.](http://www.inf.uni-konstanz.de/algo/publications/b-fabc-01.pdf)
    2. [Ulrik Brandes: On Variants of Shortest-Path Betweenness Centrality and their Generic Computation. Social Networks 30(2):136-145, 2008](http://www.inf.uni-konstanz.de/algo/publications/b-vspbc-08.pdf)
    
2. degree_product: \[weighted | unweighted\]

### Evaluation
| Notion | Metric | Global<br>Local | Topological<br>Attribute | Description |
| --- | --- | --- | --- | --- |
| R_{GC} |giant componet fraction | Global | Topological | A sudden decline of R_GC will be observed if the network disintegrates after the deletion of a certain fraction of edge |   
| \tilde{S} | normalized susceptibility | Global | Topological | obvious peak can be observed that corresponds to the precise point at which the network disintegrates |

## Datasets \[ONGOING\]

## Contribution
Feel free to open issues to report bugs or requests implemention of a specific menthod.
