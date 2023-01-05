import argparse
import logging

from common import render_graph, run_graph_search
from astar import (
    AstarGraph,
    Norm1AstarHeuristic,
    Norm2AstarHeuristic,
    WeightedAstarHeuristic,
)
from dijkstra import DijkstraGraph
from grass_fire import GrassFireGraph


def parse_args(algo_names):
    p = argparse.ArgumentParser()
    p.add_argument("algo_name", choices=algo_names)
    p.add_argument("--grid-size", "-g", type=int, default=100)
    p.add_argument("--number-obstacles", "-n", type=int, default=50)
    p.add_argument("--max-obstacle-size", "-m", type=int, default=20)
    p.add_argument("--no-render", default=False, action="store_true")
    p.add_argument("--xs", type=int, default=0)
    p.add_argument("--ys", type=int, default=0)
    p.add_argument("--xf", type=int)
    p.add_argument("--yf", type=int)
    return p.parse_args()


algo_facto = {
    "GrassFire": GrassFireGraph,
    "AstarL1": lambda max_x, max_y, cost_map: AstarGraph(
        max_x, max_y, cost_map, Norm1AstarHeuristic()
    ),
    "AstarL2": lambda max_x, max_y, cost_map: AstarGraph(
        max_x, max_y, cost_map, Norm2AstarHeuristic()
    ),
    "WAstarL1": lambda max_x, max_y, cost_map: AstarGraph(
        max_x, max_y, cost_map, WeightedAstarHeuristic(1.5, Norm1AstarHeuristic())
    ),
    "WAstarL2": lambda max_x, max_y, cost_map: AstarGraph(
        max_x, max_y, cost_map, WeightedAstarHeuristic(1.5, Norm2AstarHeuristic())
    ),
    "Dijkstra": DijkstraGraph,
    "show_path": None,
}


def run_from_cli():
    args = parse_args(algo_facto.keys())
    if args.algo_name == "show_path":
        render_graph(args)
    else:
        ctor = algo_facto[args.algo_name]
        run_graph_search(ctor, args)


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    run_from_cli()
