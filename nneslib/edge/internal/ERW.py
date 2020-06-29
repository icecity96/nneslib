import networkx as nx
import random


def edge_random_walk_k_path(graph: nx.Graph, k: int, ruo: int, beta: float):
    normlized_deg = _normalized_degree(graph)
    edge_weight = _initial_edge_weight(graph)
    for i in range(0, ruo):
        N, vn = 0, random.choice(list(graph.nodes()))
        edge_weight = _message_propagation(graph, vn, N, k, beta, edge_weight)
    return edge_weight


def _normalized_degree(graph: nx.Graph) -> dict:
    """
    .. math:: \\delta(v_n) = \\frac{|I(v_n)|}{|V|}

    where :math:`I(v_n)` represents the set of edges incident on :math:`v_n`.
    :param graph: the networkx graph object to be used.
    :return: a dict of normalized degree
    """
    return {node: len(graph.neighbors(node))/graph.number_of_nodes() for node in graph.nodes()}


def _initial_edge_weight(graph: nx.Graph) -> dict:
    edges_number = graph.number_of_edges()
    return {(u,v): 1/edges_number for u, v in graph.edges()}


def _message_propagation(graph, vn, N: int, k: int, ruo: float, edge_weight: dict) -> dict:
    T = {}
    for u, v in graph.edges():
        T[(u,v)] = 0
        T[(v,u)] = 0
    while N < k and len(graph.neighbors(vn)) > sum([T[(u,vn)] for u in graph.neighbors(vn)]):
        edges = [(u, vn) for u in graph.neighbors(vn) if T[(u, vn)] == 0]
        selected_edge = random.choice(edges)
        if selected_edge in edge_weight:
            edge_weight[selected_edge] += ruo
        else:
            edge_weight[(selected_edge[1], selected_edge[0])] += ruo
        T[selected_edge] = 1
        T[(selected_edge[1], selected_edge[0])] = 1
        vn = selected_edge[0]
        N += 1
    return edge_weight
