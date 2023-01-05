from abc import ABC, abstractmethod
from math import inf
from typing import List, Optional
import itertools
from logging import debug, info, warning
from graph import Graph, Node
import heapq


class AstarNode(Node):
    def __init__(self, x: int, y: int, cost_to_go: float) -> None:
        super().__init__(x, y, cost_to_go)
        self.h = 0.0
        self.parent: Optional[AstarNode] = None

    @property
    def f(self):
        return self.h + self.cost

    def __lt__(self, other):
        # If the f values are equal, then we take the 'closest' one (with the smallest heuristic)
        return self.f < other.f if self.f != other.f else self.h < other.h


class AstarHeuristic(ABC):
    @abstractmethod
    def __call__(self, xs: int, ys: int, xf: int, yf: int) -> float:
        pass


class Norm1AstarHeuristic(AstarHeuristic):
    def __call__(self, xs: int, ys: int, xf: int, yf: int) -> float:
        return abs(xs - xf) + abs(ys - yf)


class Norm2AstarHeuristic(AstarHeuristic):
    def __call__(self, xs: int, ys: int, xf: int, yf: int) -> float:
        return ((xs - xf) ** 2 + (ys - yf) ** 2) ** 0.5


class WeightedAstarHeuristic(AstarHeuristic):
    def __init__(self, eps: float, base_h: AstarHeuristic) -> None:
        super().__init__()
        self.h = base_h
        self.eps = eps

    def __call__(self, xs: int, ys: int, xf: int, yf: int) -> float:
        return self.eps * self.h(xs, ys, xf, yf)


class AstarGraph(Graph[AstarNode]):
    def __init__(self, max_x: int, max_y: int, cost_map, h: AstarHeuristic) -> None:
        super().__init__(max_x, max_y)
        self.h = h
        for z in range(max_x * max_y):
            x, y = self._unflatten(z)
            self._nodes.append(AstarNode(x, y, cost_map[(x, y)]))

    def compute_path(self, xs: int, ys: int, xf: int, yf: int) -> List[AstarNode]:
        self.reset_nodes()
        # In python 3, there is no heap per se, but one can use a normal list
        # and then use the functions defined in the heapq package to maintain the heap invariants
        start = self.node(xs, ys)
        start.cost = 0
        start.h = self.h(
            xs, ys, xf, yf
        )  # actually useless because the value is never read
        heap = [start]

        max_iter = 1000000
        print_period = 1000
        for n in range(max_iter):
            if n % print_period == 0:
                debug(f"Iteration {n}/{max_iter}")

            try:
                node_to_explore = heapq.heappop(heap)
            except IndexError:
                warning(
                    f"No path exists from start ({xs}, {ys}) to goal ({xf}, {yf}) after {n+1} iterations"
                )
                return []

            x = node_to_explore.x
            y = node_to_explore.y

            # Optimal graph search waits until we explore the destination,
            # NOT until we add it to our heap. Otherwise we might be missing
            # a shorter path (which might be preferable actually!)
            if x == xf and y == yf:
                info(
                    f"Found path from start ({xs}, {ys}) to goal ({xf}, {yf}) after {n+1} iterations and {n+1+len(heap)} nodes added"
                )
                return self.collect_path(node_to_explore)

            # We consider here an 8-connected grid, because why not :)
            for (dx, dy) in itertools.product([-1, 0, 1], [-1, 0, 1]):
                next_node = self.try_node(x + dx, y + dy)
                if next_node is None:
                    continue

                # 8-connected, yes, but we consider diagonal movements to be more expensive
                # half of the cost comes the current node, the other half from the next
                # (assuming center-to-center movement)
                dg = (
                    (dx**2 + dy**2) ** 0.5
                    * (next_node.cost_to_go + node_to_explore.cost_to_go)
                    * 0.5
                )
                g = node_to_explore.cost + dg

                # Already had a better path to reach this node
                if next_node.cost <= g:
                    continue

                next_node.cost = g
                next_node.parent = node_to_explore
                h = self.h(next_node.x, next_node.y, xf, yf)
                next_node.h = h
                heapq.heappush(heap, next_node)

        warning(f"Could not find a path after {max_iter} iterations")
        return []

    def reset_nodes(self):
        for n in self._nodes:
            n.cost = inf
            n.parent = None

    def collect_path(self, n: AstarNode) -> List[AstarNode]:
        path = [n]
        while path[-1].parent is not None:
            path.append(path[-1].parent)
        path.reverse()
        return path


if __name__ == "__main__":
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

    g = AstarGraph(max_x, max_y, cost_map, Norm1AstarHeuristic())
    print("Node cost map:")
    print(g.cost_to_go_str())

    xs, ys = (1, 2)

    xf, yf = (9, 0)
    path = g.compute_path(xs, ys, xf, yf)
    print(f"Path from initial point ({xs}, {ys}) to goal point ({xf}, {yf})")
    print(g.path_str(path))
