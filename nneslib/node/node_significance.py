import networkx as nx
import numpy as np

import numpy.linalg as linalg
from nneslib.classes.node_significance import NodeSignificance


def centrality_metric_spectrum(graph: nx.Graph, communities_number: int, weight: str = None) -> NodeSignificance:
    """
    Centrality metric based on the spectrum of the Adjacency Matrix.

    .. math:: P_k = \\sum_{i=1}^c \\frac{v^2_{ik}}{v^T_{i}v_i}

    wher c in the number of the communities, :math:`v_{ik}` is the kth element of :math:`v_i` and :math:`P_k` lies in [0,1]

    .. math:: I_k = P_k / c

    :param graph: the networkx graph object to be used.
    :param communities_number: the number of communities
    :param weight: If None, all edge weights are considered equal. Otherwise holds the name of the edge attribute used as weight.
    :return: an NodeSignificance object

    .. rubric:: Reference

    .. [1] Wang, Yang, Zengru Di, and Ying Fan. 2011. Identifying and Characterizing Nodes Important to Community Structure Using the Spectrum of the Graph. PLoS ONE 6: e27418. https://doi.org/10.1371/journal.pone.0027418.
    """
    matrix = nx.to_numpy_matrix(graph, weight=weight)
    eigenvalues, eigenvectors = linalg.eig(matrix)
    lagest_eigenvalues_idx = np.argpartition(-eigenvalues, communities_number)[:communities_number]
    significance = {}
    eigenvectors_dot = [np.sum([v * v for v in eigenvectors[:, i].flatten().tolist()[0]]) for i in range(len(eigenvalues))]
    for k, node_name in enumerate(list(graph.nodes())):
        significance[node_name] = sum([eigenvectors[k, idx]**2/ eigenvectors_dot[idx]
                                       for idx in lagest_eigenvalues_idx]) / communities_number
    # TODO: Distinguish Two Kinds of Importance Nodes? or not?
    return NodeSignificance(significance, graph, "centrality_metric_spectrum",
                            {"communities_number": communities_number, "weight": weight})