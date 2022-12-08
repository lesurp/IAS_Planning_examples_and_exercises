from math import inf
from typing import Optional, Tuple, List


class Node:
    def __init__(self, x: int, y: int, cost: float) -> None:
        self.cost: Optional[float] = None
        self.cost_to_go = cost
        self.x = x
        self.y = y


class Graph:
    def __init__(self, max_x: int, max_y: int, cost_map) -> None:
        self._max_x = max_x
        self._max_y = max_y
        self._nodes = []
        for z in range(max_x * max_y):
            x, y = self._unflatten(z)
            self._nodes.append(Node(x, y, cost_map[(x, y)]))

    def is_in(self, x: int, y: int) -> bool:
        return 0 <= x < self._max_x and 0 <= y < self._max_y

    def neighbors(self, node: Node) -> List[Node]:
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

    def reset_costs(self):
        for n in self._nodes:
            n.cost = None

    def initialize_costs(self, xs: int, ys: int):
        self.reset_costs()
        ns = self.node(xs, ys)
        ns.cost = 0
        nodes = [ns]
        while nodes:
            cur_n = nodes.pop()
            assert cur_n.cost is not None
            neighbors = self.neighbors(cur_n)
            to_add = []
            for next_n in neighbors:
                new_cost = cur_n.cost + next_n.cost_to_go
                if next_n.cost is not None and next_n.cost < new_cost:
                    continue
                next_n.cost = new_cost
                to_add.append(next_n)
            nodes += to_add

    def path_to(self, xf: int, yf: int) -> List[Node]:
        nf = self.node(xf, yf)
        if nf.cost is None:
            return []

        path = [nf]
        while path[-1].cost != 0:
            neighbors = self.neighbors(path[-1])
            valid_neighbors = [n for n in neighbors if n.cost is not None]
            valid_neighbors.sort(key=lambda node: node.cost)  # type: ignore
            path.append(valid_neighbors[0])
        path.reverse()
        return path

    # Helper functions
    def _flatten(self, x: int, y: int) -> int:
        return y * self._max_x + x

    def _unflatten(self, z: int) -> Tuple[int, int]:
        x = z % self._max_x
        y = (z - x) // self._max_x
        return (x, y)

    def _generic_str(self, padding, fn) -> str:
        out = ""
        for y in range(self._max_y):
            out += "".join(
                [f"{fn(self.node(x, y)):>{padding}}" for x in range(0, self._max_x)]
            )[1:]
            out += "\n"
        return out[0:-1]

    def cost_to_go_str(self) -> str:
        return self._generic_str(
            2,
            lambda node: str(int(round(node.cost_to_go)))
            if node.cost_to_go < inf
            else "X",
        )

    def total_cost_str(self) -> str:
        return self._generic_str(
            5, lambda node: node.cost if node.cost is not None else "?"
        )

    def path_str(self, path) -> str:
        return self._generic_str(
            5, lambda node: path.index(node) if node in path else "X"
        )

    def node(self, x: int, y: int) -> Node:
        return self._nodes[self._flatten(x, y)]
