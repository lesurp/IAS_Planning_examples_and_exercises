from common import run_graph_search
from grass_fire import GrassFireGraph


class Args(dict):
    def __init__(self, **entries):
        self.xs = 0
        self.ys = 0
        self.grid_size = 1000
        self.max_obstacle_size = 20
        self.number_obstacles = 50
        self.no_render = False
        self.algo_name = None
        self.xf = None
        self.yf = None
        self.__dict__.update(entries)


def run_grass_fire(args):
    args = Args(**args)
    run_graph_search(GrassFireGraph, args)


def run_astar_with_heuristic(args, astar_impl, astar_heuristic):
    args = Args(**args)
    ctor = lambda max_x, max_y, cost_map: astar_impl(
        max_x, max_y, cost_map, astar_heuristic
    )
    run_graph_search(ctor, args)
