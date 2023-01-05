#!/bin/bash

tar czf Exercise06.tar.gz --transform="flags=r;s|\(.*\).template|\1|" graph.py grass_fire.py common.py main.py jupy_main.py exercise_06.ipynb
