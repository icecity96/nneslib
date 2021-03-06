import networkx as nx
import numpy as np
from nneslib.classes.edge_significance import EdgeSignificance
from .internal import edge_random_walk_k_path


__all__ = [
    'betweenness_centrality', 'degree_product', 'diffusion_importance', 'brightness',
    'ERW_Kpath'
]


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
        for u, v in graph.edges()}
    return EdgeSignificance(significance, graph, "degree_product", {"weight": weight, "theta": theta})


def diffusion_importance(graph: nx.Graph) -> EdgeSignificance:
    """
    The diffusion importance of an edge takes disease spread process into consideration.

    .. math:: D_{e} = \\frac{n_{x \\leftarrow y} + n_{y \leftarrow x}}{2}

    where :math:`n_{x \\leftarrow y}` is the number of links of node y connecting outside the nearest neighborhood of
    node x.

    :param graph: the networkx graph object to be used. Treat it as unweighted
    :return: an EdgeSignificance object

    .. rubric:: Example

    >>> from nneslib.edge import edge_significance
    >>> import networkx as nx
    >>> G = nx.karate_club_graph()
    >>> es = edge_significance.diffusion_importance(G)

    .. rubric:: Reference

    .. [1] Liu Y, Tang M, Zhou T, et al. Improving the accuracy of the k-shell method by removing redundant links: From a perspective of spreading dynamics[J]. Scientific reports, 2015, 5: 13172.
    """
    significance = {}
    for u, v in graph.edges():
        u_neighbors, v_neighbors = graph.neighbors(u), graph.neighbors(v)
        n_uv = len([node for node in u_neighbors if graph.has_edge(v, node) and node != v])
        n_vu = len([node for node in v_neighbors if graph.has_edge(u, node) and node != u])
        significance[[u, v]] = (n_uv + n_vu)/2
    return EdgeSignificance(significance, graph, "diffusion_importance", None)


def brightness(graph: nx.Graph) -> EdgeSignificance:
    """
    The brightness of an edge can reflect the significance in maintaining global connectivity, which only depends on local information
    of network topology.

    .. math:: B_E = \\sqrt{S_xS_y}/S_E

    where x and y are the two endpoints of the edge E. S is the clique size.

    :param graph: the networkx graph object to be used
    :return: an EdgeSignificance object

    .. rubric:: Example

    >>> from nneslib.edge import edge_significance
    >>> import networkx as nx
    >>> G = nx.karate_club_graph()
    >>> es = edge_significance.brightness(G)

    .. rubric:: Reference

    .. [1]Cheng X Q, Ren F X, Shen H W, et al. Bridgeness: a local index on edge significance in maintaining global connectivity[J]. Journal of Statistical Mechanics: Theory and Experiment, 2010, 2010(10): P10011.
    """
    cliques = sorted(nx.find_cliques(graph), key=len, reverse=True)
    significance = {}
    for u, v in graph.edges():
        s_u, s_v, s_e = 0, 0, 0
        for clique in cliques:
            if s_u * s_v * s_e != 0:    # already find
                break
            if u in clique and s_u == 0:
                s_u = len(clique)
            if v in clique and s_v == 0:
                s_v = len(clique)
            if u in clique and s_e == 0 and v in clique:
                s_e = len(clique)
        significance[[u,v]] = np.sqrt(s_u * s_v) / s_e
    return EdgeSignificance(significance, graph, "brightness", None)


def ERW_Kpath(graph: nx.Graph, k: int, ruo: int, beta:float) -> EdgeSignificance:
    """
    Edge random walk K path. This method use random walk to estimate the edge k-path centrality.

    .. math:: L^k(e) = \\sum_{s \\in V}\\frac{\\delta_s^k(e)}{\\delta_s^k}

    where s is all possible source node. :math:`\\delta_s^k` is the number of k-path origin from s. :math:`\\delta_s^k(e)`
    is the number of k-path origin from s and traving from e.

    :param graph: the networkx graph object to be used
    :param k: the max path length
    :param ruo: how many times to iter
    :param beta: update step.
    :return: an EdgeSignificance object

    .. rubric:: Reference
    .. [1] Meo, Pasquale De, Emilio Ferrara, Giacomo Fiumara, and Angela Ricciardello 2013A Novel Measure of Edge Centrality in Social Networks. ArXiv.
    """
    significance = edge_random_walk_k_path(graph, k, ruo, beta)
    return EdgeSignificance(significance, graph, "ERW_Kpath", {"k": k, "ruo": ruo, "beta": beta})

