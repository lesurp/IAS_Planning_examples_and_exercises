#!/bin/bash

tar czf Exercise05.tar.gz --transform="flags=r;s|\(.*\).template|\1|" graph.py show_path.py grass_fire.py astar.py.template dijkstra.py.template
