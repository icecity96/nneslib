import unittest
import networkx as nx
from nneslib.node.node_significance import centrality_metric_spectrum, EffC


class NodeImportanceTestCase(unittest.TestCase):
    def test_centrality_metric_spectrum(self):
        """Examples from: doi:10.1371/journal.pone.0027418.g001"""
        graph = nx.Graph()
        graph.add_nodes_from([i for i in range(1, 16)])
        edges = [(8, i) for i in range(9, 16)] + [(i, i + 1) for i in range(9, 15)] + [(9, 15), (7, 15), (2, 15), (1, 15)]
        edges += [(1, i) for i in range(2, 8)] + [(i, i + 1) for i in range(2, 7)]
        graph.add_edges_from(edges)
        communities_number = 2
        node_significance = centrality_metric_spectrum(graph, communities_number)
        expected = {
            1: 0.16, 8: 0.16, 15: 0.086, 2: 0.045, 7: 0.045,
            9: 0.045, 14: 0.045, 3: 0.05, 6: 0.05, 10: 0.05,
            13: 0.05, 4: 0.052, 5: 0.052, 11: 0.052, 12: 0.052
        }
        actual = node_significance.significance
        self.assertEqual(set(expected), set(actual))
        for key in actual:
            self.assertAlmostEqual(expected[key], actual[key], delta=1e-2)

    def test_EffC(self):
        graph = nx.Graph()
        graph.add_nodes_from([i for i in range(1, 10)])
        edges = [(i, 3) for i in range(1, 8) if i != 3] + [(5, 7), (3, 9), (7, 8), (8, 9), (2, 9), (4, 5), (5, 6)]
        graph.add_edges_from(edges)
        node_significance = EffC(graph, None)
        expected = {
            1: 0.1806, 2: 0.2083, 3: 0.5215, 4: 0.2014, 5: 0.2500, 6: 0.2014, 7: 0.2361, 8: 0.1875, 9: 0.2361
        }
        actual = node_significance.significance
        self.assertEqual(set(expected), set(actual))
        for key in actual:
            self.assertAlmostEqual(expected[key], actual[key], delta=1e-4)

if __name__ == '__main__':
    unittest.main()
