from os import environ


environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import time
from collections import defaultdict
import numpy as np


import itertools
from math import inf


class Renderer:
    def __init__(self, max_x, max_y) -> None:
        pygame.init()
        width_padded = max(1024, max_x)
        self.width = max_x * int(width_padded / max_x)
        height_padded = max(1024, max_y)
        self.height = max_y * int(height_padded / max_y)
        self.max_x = max_x
        self.max_y = max_y

    @property
    def rect_width(self):
        return int(self.width / self.max_x)

    @property
    def rect_height(self):
        return int(self.height / self.max_y)

    def draw_rect(self, surface, color, x, y):
        x_rect = x * self.rect_width
        y_rect = y * self.rect_height
        rect = pygame.Rect(x_rect, y_rect, self.rect_width, self.rect_height)
        pygame.draw.rect(surface, color, rect)

    def show_path(self, name, path, cost_map):
        surface = pygame.display.set_mode((self.width, self.height))
        surface.fill(pygame.Color(255, 0, 255))
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
        pygame.quit()


def _construct_complex_map(max_x, max_y, n_obstacles, max_size):
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


def cost_map_from_args(args):
    number_obstacles = args.number_obstacles
    max_obstacle_size = args.max_obstacle_size
    max_x = args.max_x
    max_y = args.max_y
    return _construct_complex_map(max_x, max_y, number_obstacles, max_obstacle_size)


def run_graph_search(graph_ctor, args):
    render = not args.no_render
    max_x = args.max_x
    max_y = args.max_y
    xs = args.xs
    ys = args.ys
    xf = args.xf if args.xf else max_x - 1
    yf = args.yf if args.yf else max_y - 1
    algo_name = args.algo_name if args.algo_name else ""

    cost_map = cost_map_from_args(args)
    start = time.perf_counter()
    path = graph_ctor(max_x, max_y, cost_map).compute_path(xs, ys, xf, yf)
    end = time.perf_counter()
    print(f"Path search took {(end - start) * 1e3}ms, final cost: {path[-1].cost}")
    if cost_map and render:
        Renderer(max_x, max_y).show_path(algo_name, path, cost_map)


def render_graph(args):
    max_x = args.max_x
    max_y = args.max_y
    cost_map = cost_map_from_args(args)
    Renderer(max_x, max_y).show_path("show_path", [], cost_map)
