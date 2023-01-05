from common import run_graph_search
import common
from grass_fire import GrassFireGraph


class Args(dict):
    def __init__(self, **entries):
        self.xs = 0
        self.ys = 0
        self.grid_size = 1000
        self.max_x = None
        self.max_y = None
        self.max_obstacle_size = 20
        self.number_obstacles = 50
        self.no_render = False
        self.algo_name = None
        self.xf = None
        self.yf = None
        self.__dict__.update(entries)

        if self.max_y is None:
            self.max_y = self.grid_size
        if self.max_x is None:
            self.max_x = self.grid_size


def run_grass_fire(args):
    args = Args(**args)
    run_graph_search(GrassFireGraph, args)


def run_astar_with_heuristic(args, astar_impl, astar_heuristic):
    args["algo_name"] = str(args)
    args = Args(**args)
    ctor = lambda max_x, max_y, cost_map: astar_impl(
        max_x, max_y, cost_map, astar_heuristic
    )
    run_graph_search(ctor, args)


def render_graph(args):
    args = Args(**args)
    common.render_graph(args)
