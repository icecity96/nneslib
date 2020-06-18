import networkx as nx
from nneslib.classes.edge_significance import EdgeSignificance

__all__ = ['betweenness_centrality', 'degree_product']


def betweenness_centrality(graph: nx.Graph, k: int = None, normalize: bool = True,
                           weight: str = None, seed: int = None) -> EdgeSignificance:
    """
    Compute betweenness centrality for edges.

    .. math:: c_B(e) =\\sum_{s,t \\in V} \\frac{\\sigma(s, t|e)}{\\sigma(s, t)}

    :param graph: the networkx graph object to be used
    :param k: If k is not None use k node samples to estimate betweenness. The value of k = n where n is the number of nodes in the graph. Higher values give better approximation.
    :param normalize:If True the betweenness values are normalized by 2/(n(n-1)) for graphs, and 1/(n(n-1)) for directed graphs where n is the number of nodes in G.
    :param weight: If None, all edge weights are considered equal. Otherwise holds the name of the edge attribute used as weight.
    :param seed: Indicator of random number generation state. See :ref:`Randomness `. Note that this is only used if k is not None.
    :return: an EdgeSignificance object


    .. rubric:: Example

    >>> from nneslib.edge import edge_significance
    >>> import networkx as nx
    >>> G = nx.karate_club_graph()
    >>> es = edge_significance.betweenness_centrality(G)


    .. rubric:: Reference

    .. [1] A Faster Algorithm for Betweenness Centrality. Ulrik Brandes, Journal of Mathematical Sociology 25(2):163-177, 2001. http://www.inf.uni-konstanz.de/algo/publications/b-fabc-01.pdf
    .. [2] Ulrik Brandes: On Variants of Shortest-Path Betweenness Centrality and their Generic Computation. Social Networks 30(2):136-145, 2008 http://www.inf.uni-konstanz.de/algo/publications/b-vspbc-08.pdf

    .. note:: This method is implemented by Networkx

    """
    ebc = nx.edge_betweenness_centrality(graph, k, normalize, weight, seed)
    significance = {key: value for key, value in ebc.items()}
    return EdgeSignificance(significance, graph, "betweenness_centrality",
                            {"k": k, "normalize": normalize, "weight": weight, "seed": seed})


def degree_product(graph: nx.Graph, weight: str = None, theta: float = 1.0) -> EdgeSignificance:
    """
    Compute the degree product to represent the edge importance.

    .. math:: Degree(e) = (k_{u}k_{v})^\\theta

    :param graph:  the networkx graph object to be used.
    :param weight: If None, all edge weights are considered equal. Otherwise holds the name of the edge attribute used as weight.
    :param theta: a tunable parameter. default value is 1.0
    :return: an EdgeSignificance object

    .. rubric:: Example

    >>> from nneslib.edge import edge_significance
    >>> import networkx as nx
    >>> G = nx.karate_club_graph()
    >>> es = edge_significance.degree_product(G)

    .. rubric:: Reference

    .. [1] Wang W X, Chen G. Universal robustness characteristic of weighted networks against cascading failure[J]. Physical Review E, 2008, 77(2): 026101.
    .. [2] Barrat A, Barthelemy M, Pastor-Satorras R, et al. The architecture of complex weighted networks[J]. Proceedings of the national academy of sciences, 2004, 101(11): 3747-3752.
    .. [3] Tang M, Zhou T. Efficient routing strategies in scale-free networks with limited bandwidth[J]. Physical review E, 2011, 84(2): 026116.
    """
    significance = {
        [u, v]: (graph.degree(u, weight=weight) * graph.degree(v, weight=weight)) ** theta
        for u, v in graph.nodes()}
    return EdgeSignificance(significance, graph, "degree_product", {"weight": weight, "theta": theta})


def diffusion_importance(graph: nx.Graph) -> EdgeSignificance:
    """
    The diffusion importance an edge takes disease spread process into consideration.

    .. math:: D_{e} = \\frac{n_{x \\leftarrow y} + n_{y \leftarrow x}}{2}

    where :math:`n_{x \\leftarrow y}` is the number of links of node y connecting outside the nearest neighborhood of
    node x.

    :param graph: the networkx graph object to be used. Treat it as unweighted
    :return: an EdgeSignificance object

    .. rubric:: Reference

    .. [1] Liu Y, Tang M, Zhou T, et al. Improving the accuracy of the k-shell method by removing redundant links: From a perspective of spreading dynamics[J]. Scientific reports, 2015, 5: 13172.
    """