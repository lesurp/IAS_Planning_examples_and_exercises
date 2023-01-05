from math import inf
from typing import List
from graph import Graph, Node


class GrassFireNode(Node):
    def __init__(self, x: int, y: int, cost_to_go: float) -> None:
        self.cost_to_go = cost_to_go
        self.x = x
        self.y = y


class GrassFireGraph(Graph[GrassFireNode]):
    def __init__(self, max_x: int, max_y: int, cost_map) -> None:
        super().__init__(max_x, max_y)
        for z in range(max_x * max_y):
            x, y = self._unflatten(z)
            self._nodes.append(GrassFireNode(x, y, cost_map[(x, y)]))

    ### Impl
    def compute_path(self, xs: int, ys: int, xf: int, yf: int) -> List[GrassFireNode]:
        self.initialize_costs(xs, ys)
        return self.path_to(xf, yf)

    ### GrassFire specific
    def neighbors(self, node: GrassFireNode) -> List[GrassFireNode]:
        neighbors = []
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x = node.x + dx
            y = node.y + dy
            if not self.is_in(x, y):
                continue
            n = self.node(x, y)
            if n.cost_to_go < inf:
                neighbors.append(n)
        return neighbors

    def initialize_costs(self, xs: int, ys: int):
        self.reset_costs()
        ns = self.node(xs, ys)
        ns.cost = 0
        nodes = [ns]
        i = 0
        while nodes:
            i += 1
            cur_n = nodes.pop()
            assert cur_n.cost is not inf
            neighbors = self.neighbors(cur_n)
            to_add = []
            for next_n in neighbors:
                new_cost = cur_n.cost + next_n.cost_to_go
                if next_n.cost <= new_cost:
                    continue
                next_n.cost = new_cost
                to_add.append(next_n)
            nodes += to_add
            nodes.sort(key=lambda n: -n.cost)

    def path_to(self, xf: int, yf: int) -> List[GrassFireNode]:
        nf = self.node(xf, yf)
        if nf.cost is inf:
            return []

        path = [nf]
        while path[-1].cost != 0:
            neighbors = self.neighbors(path[-1])
            valid_neighbors = [n for n in neighbors if n.cost is not inf]
            valid_neighbors.sort(key=lambda node: node.cost)  # type: ignore
            path.append(valid_neighbors[0])
        path.reverse()
        return path

    def total_cost_str(self) -> str:
        return self._generic_str(
            5, lambda node: node.cost if node.cost is not inf else "?"
        )

    def reset_costs(self):
        for n in self._nodes:
            n.cost = inf


def main():
    from collections import defaultdict

    # nodes will, by default, have a cost-to-go of 1
    cost_map = defaultdict(lambda: 1.0)

    # assuming our grid goes from [0;max_x[ * [0;max_y[
    max_x = 10
    max_y = 5

    # and adding some obstacles to make our problem less trivial
    for x in range(3, 9):
        for y in range(3):
            cost_map[(x, y)] = inf

    g = GrassFireGraph(max_x, max_y, cost_map)
    print("Node cost map:")
    print(g.cost_to_go_str())

    xs, ys = (1, 2)
    g.initialize_costs(xs, ys)
    print(f"Total cost-to-go map, initial point at ({xs}, {ys})")
    print(g.total_cost_str())

    xf, yf = (9, 0)
    path = g.path_to(xf, yf)
    print(f"Path from initial point ({xs}, {ys}) to goal point ({xf}, {yf})")
    print(g.path_str(path))


if __name__ == "__main__":
    main()
