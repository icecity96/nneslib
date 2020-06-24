import unittest
from nneslib.evaluation.community_structure import significance_index
import networkx as nx


class MyTestCase(unittest.TestCase):
    def test_significant_index(self):
        """Examples from: doi:10.1371/journal.pone.0027418.g001"""
        graph = nx.Graph()
        graph.add_nodes_from([i for i in range(1, 16)])
        edges = [(8, i) for i in range(9, 16)] + [(i, i + 1) for i in range(9, 15)] + [(9, 15), (7, 15), (2, 15), (1, 15)]
        edges += [(1, i) for i in range(2, 8)] + [(i, i + 1) for i in range(2, 7)]
        graph.add_edges_from(edges)
        communities_number = 2
        H_oring = significance_index(graph, communities_number)
        expected = {
            1: -0.145, 8: -0.145, 15: 0.116, 2: 0.04, 7: 0.04, 9: 0.04, 14: 0.04,
            3: -0.021, 6: -0.021, 10: -0.021, 13: -0.021, 4: -0.054, 5: -0.054,
            11: -0.054, 12: -0.054
        }
        for key in expected:
            subgraph = graph.subgraph([node for node in graph.nodes() if node != key])
            H_remove = significance_index(subgraph, communities_number)
            self.assertAlmostEqual(expected[key], H_remove - H_oring, delta=1e-2)


if __name__ == '__main__':
    unittest.main()
