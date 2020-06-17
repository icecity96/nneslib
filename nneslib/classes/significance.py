import networkx as nx
import json


class Significance(object):
    def __init__(self, significances: dict, graph: nx.Graph, method_name: str, method_parameters: dict = None):
        """
        Significances representations
        :param significances: a dict of {node : significance} or {source: {target: significance}}
        :param graph: networkx graph object
        :param method_name: algorithm used to generate this significances result
        :param method_parameters: the parameters used by method.
        """
        self.significance = significances
        self.graph = graph
        self.method_name = method_name
        self.method_parameters = method_parameters

    def write_to_json(self, filepath: str, **kwargs) -> None:
        """
        Generate a JSON formatted representation of the Significance. And write it to a file.
        :param filepath: the file path to write
        :param kwargs: additional keyword arguments
        """
        significances = {"significance": self.significance, "algorithm": self.method_name,
                         "params": self.method_parameters}
        json.dump(significances, open(filepath, 'w', encoding='utf8'), **kwargs)

    def describe(self, display_params: bool = True, precision: int = 3) -> str:
        pass
