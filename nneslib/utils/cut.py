import networkx as nx
from typing import List


def ratio_cut(graph: nx.Graph, sequences: List[list]) -> float:
    """
    RatioCut is a common objective function to encode mincut problems information.

    .. math:: RatioCut(C_1,\\dots,C_c) = \\sum_{i=1}^c \\frac{R(C_i, \\bar{C}_i)}{|C_i|}

    where the :math:`|C_i|` is the size of the community. and :math:`R` is the size of the cut between two sets of nodes.
    :param graph: the networkx graph object to be used
    :param sequences: A list of sequences of nodes in graph
    :return: The score of the RatioCut
    """
    ratiocut = sum([nx.cut_size(graph, sequence)/len(sequence) for sequence in sequences])
    return ratiocut
