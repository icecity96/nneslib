import networkx as nx
import numpy as np


def significance_index(graph: nx.Graph, communities_number: int, weight: str = None) -> float:
    """
    Measure significance of communities structure and independent of the partition algorithm.

    .. math:: H = \\frac{n}{\\bar{k}\\sum_{j=c+1}^n \\frac{1}{|\\bar{\\beta}-\\beta_j|}}

    where :math:`\\beta` is the eigenvalue of the graph Laplacian, :math:`\\bar{\\beta}` is the average value of
    :math:`\\beta_2` through :math:`\\beta_c`, :math:`\\bar{k}` is the average degree of the network and n is the
    number of vertices in the network.

    :param graph: the network graph object to be used
    :param communities_number: the number of communities
    :param weight: If None, all edge weights are considered equal. Otherwise holds the name of the edge attribute used as weight.
    :return: the significance of communities structure

    .. rubric:: Example
    >>> from nneslib.evaluation.community_structure import significance_index
    >>> import networkx as nx
    >>> G = nx.karate_club_graph()
    >>> significance_index(G, 2)

    .. note:: This method argues the significance of community structure should be the property of network itself, which
    is independent of the partition algorithm and can be evaluated without knowing the exact communities.

    .. reverse:: Reference
    .. [1] Hu, Yanqing, Yiming Ding, Ying Fan, and Zengru Di. 2010. How to Measure Significance of Community Structure in Complex Networks. arXiv.

    """
    n = graph.number_of_nodes()
    k = np.mean([d[1] for d in list(graph.degree(weight=weight))])
    eigenvalues = nx.laplacian_spectrum(graph, weight)  # eigenvalues in ascending order
    beta = np.mean(eigenvalues[1:communities_number])  # the average value of beta_2 through beta_c
    amplification_coeff = sum([1 / (abs(beta - eigenvalue) + 1e-7)
                               for eigenvalue in
                               eigenvalues[communities_number:]])  # plus 1e-7 to prevent divide by zero
    H: float = n / (k * amplification_coeff)
    return H
