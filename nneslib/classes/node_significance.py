from nneslib.classes.significance import Significance
import networkx as nx
import numpy as np


class NodeSignificance(Significance):
    def __init__(self, significances: dict, graph: nx.Graph, method_name: str,
                 method_parameters: dict = None, attrs: dict = None):
        super().__init__(significances, graph, method_name, method_parameters)
        self.attrs = attrs

    def get(self, node) -> float:
        """
        Get node's significance by node id

        :param node: node id
        :return: the significance of the node
        :raise: `NodeNotFound` if the node doesn't exist
        """
        if node in self.significance.keys():
            raise nx.NodeNotFound(f"Node {node} is not in G")
        return self.significance[node]
