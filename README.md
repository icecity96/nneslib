# NNESLIB
nneslib is a python library for evaluating Network Nodes or Edges Significance (NNES). 
This Library is written in pure Python and based on Networkx.

> nneslib is forced to undirected graph. Directed graph may be considered in next version of

[TOC]

## Implemented Methods
### Node
1. centrality_metric_spectrum: \[weighted | unweighted\]
    1. [Wang, Yang, Zengru Di, and Ying Fan. 2011. Identifying and Characterizing Nodes Important to Community Structure Using the Spectrum of the Graph. PLoS ONE 6: e27418.](https://doi.org/10.1371/journal.pone.0027418)
### Edge
1. betweenness_centrality: \[weighted | unweighted\]
    1. [A Faster Algorithm for Betweenness Centrality. Ulrik Brandes, Journal of Mathematical Sociology 25(2):163-177, 2001.](http://www.inf.uni-konstanz.de/algo/publications/b-fabc-01.pdf)
    2. [Ulrik Brandes: On Variants of Shortest-Path Betweenness Centrality and their Generic Computation. Social Networks 30(2):136-145, 2008](http://www.inf.uni-konstanz.de/algo/publications/b-vspbc-08.pdf)
    
2. degree_product: \[weighted | unweighted\]
    1. Wang W X, Chen G. Universal robustness characteristic of weighted networks against cascading failure[J]. Physical Review E, 2008, 77(2): 026101.
    2. Barrat A, Barthelemy M, Pastor-Satorras R, et al. The architecture of complex weighted networks[J]. Proceedings of the national academy of sciences, 2004, 101(11): 3747-3752.
    3. Tang M, Zhou T. Efficient routing strategies in scale-free networks with limited bandwidth[J]. Physical review E, 2011, 84(2): 026116.

3. diffusion_importance: \[unweighted\]
    1. Liu Y, Tang M, Zhou T, et al. Improving the accuracy of the k-shell method by removing redundant links: From a perspective of spreading dynamics[J]. Scientific reports, 2015, 5: 13172.

4. brightness: \[unweighted\]
    1. Cheng X Q, Ren F X, Shen H W, et al. Bridgeness: a local index on edge significance in maintaining global connectivity[J]. Journal of Statistical Mechanics: Theory and Experiment, 2010, 2010(10): P10011.

5. ERW_Kpath: \[unweighted]:
    1. Meo, Pasquale De, Emilio Ferrara, Giacomo Fiumara, and Angela Ricciardello 2013A Novel Measure of Edge Centrality in Social Networks. ArXiv.
### Evaluation
| Notion | Metric | Global<br>Local | Topological<br>Linalg | Description |
| --- | --- | --- | --- | --- |
| R_{GC} |giant componet fraction | Global | Topological | A sudden decline of R_GC will be observed if the network disintegrates after the deletion of a certain fraction of edge |   
| \tilde{S} | normalized susceptibility | Global | Topological | obvious peak can be observed that corresponds to the precise point at which the network disintegrates |
| H | significance of communities structure | Global | Linalg | Measure significance of communities structure and independent of the partition algorithm.|
## Datasets \[ONGOING\]

## Contribution
Feel free to open issues to report bugs or requests implemention of a specific menthod.
