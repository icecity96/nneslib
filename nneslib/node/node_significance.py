import networkx as nx
import numpy as np

import numpy.linalg as linalg
from nneslib.classes.node_significance import NodeSignificance

__all__ = [
    "centrality_metric_spectrum", "degree_centrality", "betweenness_centrality", "closeness_centrality"
]


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


def degree_centrality(graph: nx.Graph) -> NodeSignificance:
    """
    Degree centrality.

    .. math:: C_D(v) = \\sum_{u \in V}a_{u,v}

    :param graph: the graph object to be used
    :return: a NodeSignificance object
    """
    significance = nx.degree_centrality(graph)
    return NodeSignificance(significance, graph, "degree_centrality", None)


def betweenness_centrality(graph: nx.Graph, k: int = None,
                           normalized: bool = True, weight: str = None) -> NodeSignificance:
    """
    Compute the shortest-path betweenness centrality for nodes.

    Betweenness centrality of a node $v$ is the sum of the
    fraction of all-pairs shortest paths that pass through $v$

    .. math::

       c_B(v) =\sum_{s,t \in V} \frac{\sigma(s, t|v)}{\sigma(s, t)}

    where $V$ is the set of nodes, $\sigma(s, t)$ is the number of
    shortest $(s, t)$-paths,  and $\sigma(s, t|v)$ is the number of
    those paths  passing through some  node $v$ other than $s, t$.
    If $s = t$, $\sigma(s, t) = 1$, and if $v \in {s, t}$,
    $\sigma(s, t|v) = 0$ [2]_.

    :param graph: A networkx graph
    :param k: If k is not None use k node samples to estimate betweenness.
      The value of k <= n where n is the number of nodes in the graph.
      Higher values give better approximation.
    :param normalized: If True the betweenness values are normalized by `2/((n-1)(n-2))`
      for graphs, and `1/((n-1)(n-2))` for directed graphs where `n`
      is the number of nodes in G.
    :param weight: If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.
    :return: an NodeSignificance object
    """
    significance = nx.betweenness_centrality(graph, k=k, normalized=normalized, weight=weight)
    return NodeSignificance(significance, graph, "betweenness_centrality",
                            {"k": k, "normalized": normalized, "weight": weight})


def closeness_centrality(graph: nx.Graph, distance: str = None, wf_improved: bool = True) -> NodeSignificance:
    """
   Compute closeness centrality for nodes.

    Closeness centrality [1]_ of a node `u` is the reciprocal of the
    average shortest path distance to `u` over all `n-1` reachable nodes.

    .. math::

        C(u) = \frac{n - 1}{\sum_{v=1}^{n-1} d(v, u)},

    where `d(v, u)` is the shortest-path distance between `v` and `u`,
    and `n` is the number of nodes that can reach `u`. Notice that the
    closeness distance function computes the incoming distance to `u`
    for directed graphs. To use outward distance, act on `G.reverse()`.

    Notice that higher values of closeness indicate higher centrality.

    Wasserman and Faust propose an improved formula for graphs with
    more than one connected component. The result is "a ratio of the
    fraction of actors in the group who are reachable, to the average
    distance" from the reachable actors [2]_. You might think this
    scale factor is inverted but it is not. As is, nodes from small
    components receive a smaller closeness value. Letting `N` denote
    the number of nodes in the graph,

    .. math::

        C_{WF}(u) = \frac{n-1}{N-1} \frac{n - 1}{\sum_{v=1}^{n-1} d(v, u)},

    :param graph: the networkx graph object to be used
    :param distance: Use the specified edge attribute as the edge distance in shortest
      path calculations
    :param wf_improved: If True, scale by the fraction of nodes reachable. This gives the
      Wasserman and Faust improved formula. For single component graphs
      it is the same as the original formula.
    :return: a NodeSignificance object
    """
    significance = nx.closeness_centrality(graph, distance=distance, wf_improved=wf_improved)
    return NodeSignificance(significance, graph, "closeness_centrality",
                            {"distance": distance, "wf_improved": wf_improved})