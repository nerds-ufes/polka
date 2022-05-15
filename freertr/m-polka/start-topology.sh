#!/bin/bash

RTR=<freertr path>
HWSW=<router files path>

tmux new-session -d -s rare 'java -jar '$RTR' routersc '$HWSW'r1-hw.txt '$HWSW'r1-sw.txt'
tmux split-window -v -t 0 -p 50
tmux send 'java -jar '$RTR' routersc '$HWSW'r2-hw.txt '$HWSW'r2-sw.txt' ENTER;
tmux split-window -h -t 0 -p 50
tmux send 'java -jar '$RTR' routersc '$HWSW'r3-hw.txt '$HWSW'r3-sw.txt' ENTER;
tmux split-window -h -t 2 -p 50
tmux send 'java -jar '$RTR' routersc '$HWSW'r4-hw.txt '$HWSW'r4-sw.txt' ENTER;
tmux split-window -v -t 0 -p 50
tmux send 'java -jar '$RTR' routersc '$HWSW'r7-hw.txt '$HWSW'r7-sw.txt' ENTER;
tmux split-window -v -t 2 -p 50
tmux send 'java -jar '$RTR' routersc '$HWSW'r6-hw.txt '$HWSW'r6-sw.txt' ENTER;
tmux split-window -v -t 2 -p 50
tmux send 'java -jar '$RTR' routersc '$HWSW'r5-hw.txt '$HWSW'r5-sw.txt' ENTER;
tmux select-layout tiled
tmux a;
