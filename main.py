import argparse
import cProfile
import itertools
import logging
import time
from collections import defaultdict
from math import cos, inf
from os import environ

import numpy as np

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

from astar import (
    AstarGraph,
    Norm1AstarHeuristic,
    Norm2AstarHeuristic,
    WeightedAstarHeuristic,
)
from dijkstra import DijkstraGraph
from grass_fire import GrassFireGraph
from show_path import ShowPathGraph


class Renderer:
    def __init__(self, max_x, max_y) -> None:
        pygame.init()
        self.width = 1024
        self.height = 1024
        self.max_x = max_x
        self.max_y = max_y

    @property
    def rect_width(self):
        return int(512 / self.max_x)

    @property
    def rect_height(self):
        return int(512 / self.max_y)

    def draw_rect(self, surface, color, x, y):
        x_rect = x * self.rect_width
        y_rect = y * self.rect_height
        rect = pygame.Rect(x_rect, y_rect, self.rect_width, self.rect_height)
        pygame.draw.rect(surface, color, rect)

    def show_path(self, name, path, cost_map):
        surface = pygame.display.set_mode((512, 512))
        pygame.display.set_caption(name)
        for (x, y) in itertools.product(range(self.max_x), range(self.max_y)):
            cost = cost_map[(x, y)]
            if cost == inf:
                color = pygame.Color(0, 0, 0)
            else:
                alpha = (cost - 1.0) / 9
                color = pygame.Color(int(255.0 * alpha), int(255.0 * (1.0 - alpha)), 0)
            self.draw_rect(surface, color, x, y)

        for node in path:
            self.draw_rect(surface, pygame.Color(64, 64, 128), node.x, node.y)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()


def construct_complex_map(max_x, max_y, n_obstacles, max_size):
    cost_map = defaultdict(lambda: 1.0)

    rng = np.random.default_rng(0)
    for _ in range(n_obstacles):
        xmin = rng.integers(0, max_x)
        ymin = rng.integers(0, max_y)
        xmax = rng.integers(0, max_size) + xmin + 1
        ymax = rng.integers(0, max_size) + ymin + 1

        # Gives a small chance to make obstacles crossable at a higher cost
        if rng.random() < 0.2:
            c = 8.0 * rng.random() + 2.0
        else:
            c = inf

        for (x, y) in itertools.product(range(xmin, xmax), range(ymin, ymax)):
            cost_map[(x, y)] = c

    return cost_map


def parse_args(algo_names):
    p = argparse.ArgumentParser()
    p.add_argument("algo_name", choices=algo_names)
    p.add_argument("--grid-size", "-g", type=int, default=100)
    p.add_argument("--number-obstacles", "-n", type=int, default=50)
    p.add_argument("--max-obstacle-size", "-m", type=int, default=20)
    p.add_argument("--no-render", default=False, action="store_true")
    return p.parse_args()


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

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
        "show_path": ShowPathGraph,
    }
    args = parse_args(algo_facto.keys())
    max_x = args.grid_size
    max_y = args.grid_size
    cost_map = construct_complex_map(
        max_x, max_y, args.number_obstacles, args.max_obstacle_size
    )
    if not args.no_render:
        r = Renderer(max_x, max_y)
    else:
        r = None
    xs, ys = (0, 0)
    xf, yf = (30, max_y - 1)
    # xf, yf = (max_x - 1, max_y - 1)
    a = algo_facto[args.algo_name](max_x, max_y, cost_map)
    start = time.perf_counter()
    path = a.compute_path(xs, ys, xf, yf)
    end = time.perf_counter()
    print(f"Path search took {(end - start) * 1e3}ms, final cost: {path[-1].g}")
    if r is not None:
        r.show_path(args.algo_name, path, cost_map)


if __name__ == "__main__":
    main()
