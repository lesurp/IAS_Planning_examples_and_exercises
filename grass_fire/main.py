from grass_fire import Graph
from collections import defaultdict
from math import inf


def main():
    # nodes will, by default, have a cost-to-go of 1
    cost_map = defaultdict(lambda: 1.0)

    # assuming our grid goes from [0;max_x[ * [0;max_y[
    max_x = 10
    max_y = 5

    # and adding some obstacles to make our problem less trivial
    for x in range(3, 9):
        for y in range(3):
            cost_map[(x, y)] = inf

    g = Graph(max_x, max_y, cost_map)
    print("Node cost map:")
    print(g.cost_to_go_str())

    xs, ys = (1, 2)
    g.initialize_costs(xs, ys)
    print(f"Total cost-to-go map, initial point at ({xs}, {ys})")
    print(g.total_cost_str())

    xf, yf = (9, 0)
    path = g.path_to(xf, yf)
    print(f"Path from initial point ({xs}, {ys}) to goal point ({xf}, {yf})")
    print(g.path_str(path))
    # kprint("".join(str((n.x, n.y)) + ", " for n in path)[0:-2])


if __name__ == "__main__":
    main()
