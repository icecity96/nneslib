import networkx as nx
from nneslib.classes.node_significance import NodeSignificance


def _efficiency(shortest_path: dict, source, target, removed_node=None, graph: nx.Graph = None, weight=None) -> float:
    """
    The efficiency is equal to the inverse of the shortest path length
    :param shortest_path:
    :param source: source node
    :param target: target node
    :param removed_node: efficiency after removing a node
    :param graph: the graph object to be used (will be ignored if removed_node is None)
    :param weight: If None, every edge has weight/distance/cost 1. If a string, use this edge attribute as the edge
    weight. Any edge attribute not present defaults to 1. This should be same with shortest_path.
    :return: the efficiency of <source, target>
    """
    if removed_node is None:
        distance = shortest_path[source].get(target, [])
        # if there is no path between source and target, return 0
        return 0 if len(distance) == 0 else 1 / (len(distance) - 1)
    else:
        if removed_node == source or removed_node == target:
            return 0
        distance = shortest_path[source].get(target, [])
        if len(distance) == 0:  # if there is no path, remove node there still no path
            return 0
        if removed_node not in distance:  # if removed_node not in the shortest-path, the efficiency will not change
            return 1 / (len(distance) - 1)
        subgraph = graph.subgraph([node for node in graph.nodes() if node != removed_node])
        try:
            distance = nx.shortest_path(subgraph, source, target, weight=weight)
        except:
            distance = []
        return 0 if len(distance) == 0 else 1 / (len(distance) - 1)


def efficiency_centrality(graph: nx.Graph, weight: str = None) -> dict:
    shortest_path = nx.shortest_path(graph, weight=weight)
    nodes = list(graph.nodes())
    E = sum([_efficiency(shortest_path, source, target) for index, source in enumerate(nodes[:-1])
             for target in nodes[index + 1:]]) / (len(nodes) * len(nodes) - len(nodes))
    significance = {}
    # removed_N = len(nodes) - 1
    removed_N = len(nodes)
    for node in nodes:
        E_hat = sum([_efficiency(shortest_path, source, target, node, graph, weight)
                     for index, source in enumerate(nodes[:-1]) for target in nodes[index + 1:]])
        E_hat /= (removed_N * removed_N - removed_N)
        significance[node] = (E - E_hat) / E
    return significance
