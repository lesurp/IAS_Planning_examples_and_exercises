import unittest
from collections import defaultdict
from math import inf

from grass_fire import GrassFireGraph


class TestGraph(unittest.TestCase):
    def _basic_graph(self) -> Graph:
        max_x = 5
        max_y = 3
        cost_map = defaultdict(lambda: 1.0)
        return Graph(max_x, max_y, cost_map)

    def test_initialize_costs(self):
        g = self._basic_graph()
        g.initialize_costs(0, 0)
        for x in range(g._max_x):
            for y in range(g._max_y):
                n = g.node(x, y)
                # no obstacle, should be just Hamming distance for every node
                expected_cost = x + y
                self.assertEqual(n.cost, expected_cost)

    def test_is_in(self):
        g = self._basic_graph()
        is_in = [(0, 0), (2, 2), (4, 2)]
        for (x, y) in is_in:
            self.assertTrue(g.is_in(x, y))

    def test_is_not_in(self):
        g = self._basic_graph()
        is_in = [(-1, 0), (0, -1), (1, -1), (-1, 1), (20, 3), (5, 2), (4, 3), (5, 3)]
        for (x, y) in is_in:
            self.assertFalse(g.is_in(x, y))

    def test_get_neighbors(self):
        g = self._basic_graph()
        neighbors = g.neighbors(g.node(1, 1))
        expected = set([(0, 1), (2, 1), (1, 0), (1, 2)])
        actual = set([(n.x, n.y) for n in neighbors])
        self.assertEqual(actual, expected)

    def test_get_neighbors_border(self):
        g = self._basic_graph()
        neighbors = g.neighbors(g.node(4, 2))
        expected = set([(3, 2), (4, 1)])
        actual = set([(n.x, n.y) for n in neighbors])
        self.assertEqual(actual, expected)

    def test_flatten_unflatten(self):
        g = self._basic_graph()
        xy_to_expected = [
            ((0, 0), 0),
            ((1, 0), 1),
            ((4, 0), 4),
            ((0, 1), 5),
            ((1, 1), 6),
            ((0, 2), 10),
            ((4, 2), 14),
        ]

        for ((x, y), z) in xy_to_expected:
            self.assertEqual(g._flatten(x, y), z)
            self.assertEqual(g._unflatten(z), (x, y))

    def test_simple_creation(self):
        g = self._basic_graph()
        self.assertEqual(len(g._nodes), 15)

    def test_simple_str_representation(self):
        g = self._basic_graph()
        s = g.cost_to_go_str()
        expected_s = "1 1 1 1 1\n1 1 1 1 1\n1 1 1 1 1"
        self.assertEqual(s, expected_s)

    def _graph_with_obstacles(self) -> Graph:
        max_x = 5
        max_y = 3
        cost_map = defaultdict(lambda: 1.0)
        cost_map[(1, 0)] = inf
        cost_map[(1, 1)] = inf
        cost_map[(2, 0)] = inf
        cost_map[(2, 1)] = inf
        return Graph(max_x, max_y, cost_map)

    def test_obstacle_repr(self):
        g = self._graph_with_obstacles()
        s = g.cost_to_go_str()
        expected_s = "1 X X 1 1\n1 X X 1 1\n1 1 1 1 1"
        self.assertEqual(s, expected_s)


if __name__ == "__main__":
    unittest.main()
