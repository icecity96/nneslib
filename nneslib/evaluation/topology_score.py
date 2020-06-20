import networkx as nx
from collections import Counter


def giant_component_fraction(graph: nx.Graph) -> float:
    """
    The fraction of nodes contained in the giant component.

    .. math:: R_{GC} = \\frac{|GC|}{|G|}

    :param graph: the graph/graph_view object to be used
    :return: the fraction of nodes contained in the giant component
    """
    # obtain the biggest component
    giant_component = sorted(nx.connected_components(graph), key=len, reverse=True)[0]
    return len(giant_component) / graph.number_of_nodes()


def normalized_susceptibility(graph: nx.Graph) -> float:
    """
    Normalized susceptibility is defined as:

    .. math:: \\tilde{S} = \\sum_{s < s_{max}}\\frac{n_ss^2}{N}

    where :math:`n_s` is the number of components with size :math:`s`. :math:`N` is the size of the whole network,
    and the sum runs over all components but the largest one.

    :param graph: the graph/graph_view object to be used
    :return: the normalized susceptibility of the graph
    """
    connected_components = sorted(nx.connected_components(graph), key=len, reverse=True)[1:]  # all but largest
    components_size_count = Counter([len(component) for component in connected_components])
    N = graph.number_of_nodes()
    return sum([value * key * key / N for key, value in components_size_count.items()])
