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
        self.g = inf
        self.h = 0.0
        self.parent: Optional[AstarNode] = None

    @property
    def f(self):
        return self.h + self.g

    @property
    def dg(self):
        return self.cost_to_go

    def __lt__(self, other):
        # If the f values are equal, then we take the 'closest' one (with the smallest heuristic)
        return self.f < other.f if self.f != other.f else self.h < other.h


class AstarHeuristic(ABC):
    @abstractmethod
    def __call__(self, xs: int, ys: int, xf: int, yf: int) -> float:
        pass


# TODO
class Norm1AstarHeuristic(AstarHeuristic):
    pass


# TODO
class Norm2AstarHeuristic(AstarHeuristic):
    pass


# TODO
class WeightedAstarHeuristic(AstarHeuristic):
    pass


class AstarGraph(Graph[AstarNode]):
    def __init__(self, max_x: int, max_y: int, cost_map, h: AstarHeuristic) -> None:
        super().__init__(max_x, max_y)
        self.h = h
        for z in range(max_x * max_y):
            x, y = self._unflatten(z)
            self._nodes.append(AstarNode(x, y, cost_map[(x, y)]))

    # TODO
    def compute_path(self, xs: int, ys: int, xf: int, yf: int) -> List[AstarNode]:
        pass

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
