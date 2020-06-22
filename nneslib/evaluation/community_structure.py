import networkx as nx


def significance_index(graph: nx.Graph) -> float:
    """
    Measure significance of communities structure and independent of the partition algorithm.

    .. math:: H = \\frac{n}{\\bar{k}\\sum_{j=c+1}^n \\frac{1}{|\\bar{\\beta}-\\beta_j|}}

    :param graph: the network graph object to be used
    :return:

    .. note:: This method argues the significance of community structure should be the property of network itself, which
    is independent of the partition algorithm and can be evaluated without knowing the exact communities.

    .. reverse:: Reference
    .. [1] Hu, Yanqing, Yiming Ding, Ying Fan, and Zengru Di. 2010. How to Measure Significance of Community Structure in Complex Networks. arXiv.

    """
    raise NotImplemented()