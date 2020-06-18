from nneslib.classes.significance import Significance
import networkx as nx
import numpy as np


class EdgeSignificance(Significance):
    def __init__(self, significances: dict, graph: nx.Graph, method_name: str, method_parameters: dict = None):
        super().__init__(significances, graph, method_name, method_parameters)
        self.significance_matrix, self.vertices_dict = self._get_numpy_significance_matrix()

    def _get_numpy_significance_matrix(self):
        """
        Get a |V| * |V| numpy matrix format representation of all edges.

        :return: an n*n matrix of significance and a n-length node name dict.
        """
        vertices_list: list = list(self.graph.nodes())
        vertices_dict: dict = {key: index for index, key in enumerate(vertices_list)}
        significance_matrix: np.ndarray = np.zeros((len(vertices_list), len(vertices_list)))
        for edge, significance in self.significance.items():
            source, target = edge[0], edge[1]
            source, target = vertices_dict[source], vertices_dict[target]
            significance_matrix[source][target] = significance
            if not self.graph.is_directed():  # For undirected graph A[u][v] == A[v][u]
                significance_matrix[target][source] = significance
        return significance_matrix, vertices_dict

    def get(self, source, target) -> float:
        """
        Get edge significance by name

        :param source: source node label
        :param target: target node label
        :raises: `NodeNotFound` if source or target not in the vertices_dict
        :return: the significance of edge (source,target)
        """
        if source not in self.vertices_dict.keys():
            raise nx.NodeNotFound(f"Source {source} is not in G")
        if target not in self.vertices_dict.keys():
            raise nx.NodeNotFound(f"Target {target} is not in G")
        source, target = self.vertices_dict[source], self.vertices_dict[target]
        return self.significance_matrix[source][target]