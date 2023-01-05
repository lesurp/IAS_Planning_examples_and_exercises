from abc import ABC, abstractmethod
from math import inf
from typing import Generic, Tuple, List, Optional, TypeVar


class Node(ABC):
    def __init__(self, x: int, y: int, cost_to_go: float) -> None:
        self.x = x
        self.y = y
        self.cost_to_go = cost_to_go
        self.cost = inf


NodeImpl = TypeVar("NodeImpl", bound=Node)


class Graph(ABC, Generic[NodeImpl]):
    def __init__(self, max_x: int, max_y: int) -> None:
        self._max_x = max_x
        self._max_y = max_y
        self._nodes = []

    @abstractmethod
    def compute_path(self, xs: int, ys: int, xf: int, yf: int) -> List[NodeImpl]:
        pass

    # Helper functions
    @property
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y

    def is_in(self, x: int, y: int) -> bool:
        return 0 <= x < self._max_x and 0 <= y < self._max_y

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

    def path_str(self, path) -> str:
        return self._generic_str(
            5, lambda node: path.index(node) if node in path else "X"
        )

    def node(self, x: int, y: int) -> NodeImpl:
        return self._nodes[self._flatten(x, y)]

    def try_node(self, x: int, y: int) -> Optional[NodeImpl]:
        if self.is_in(x, y):
            return self.node(x, y)
        else:
            return None
