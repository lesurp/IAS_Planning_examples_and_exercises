from astar import AstarGraph, AstarHeuristic


class NullAstarHeuristic(AstarHeuristic):
    def __call__(self, *_) -> float:
        return 0.0


# Yes, it's that simple!
class DijkstraGraph(AstarGraph):
    def __init__(self, max_x: int, max_y: int, cost_map) -> None:
        super().__init__(max_x, max_y, cost_map, NullAstarHeuristic())
