#!/bin/bash
# Copyright [2019-2022] Universidade Federal do Espirito Santo
#                       Instituto Federal do Espirito Santo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
tmux new-session -d -s rare 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/ams0001-hw.txt /freertr/everson/polka/rare/ams0001-sw.txt' 
tmux split-window -v -t 0 -p 50 
tmux send 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/fra0001-hw.txt /freertr/everson/polka/rare/fra0001-sw.txt' ENTER; 
tmux split-window -h -t 0 -p 50
tmux send 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/gva0001-hw.txt /freertr/everson/polka/rare/gva0001-sw.txt' ENTER;
tmux split-window -h -t 2 -p 50
tmux send 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/rio0001-hw.txt /freertr/everson/polka/rare/rio0001-sw.txt' ENTER;
tmux split-window -v -t 0 -p 50
tmux send 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/tcd0021-hw.txt /freertr/everson/polka/rare/tcd0021-sw.txt' ENTER;
tmux split-window -v -t 2 -p 50
tmux send 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/par0101-hw.txt /freertr/everson/polka/rare/par0101-sw.txt' ENTER;
tmux split-window -v -t 4 -p 50
tmux send 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/poz0001-hw.txt /freertr/everson/polka/rare/poz0001-sw.txt' ENTER;
tmux split-window -v -t 6 -p 50
tmux send 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/bud0001-hw.txt /freertr/everson/polka/rare/bud0001-sw.txt' ENTER;
tmux split-window -v -t 6 -p 50
tmux send 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/pra0101-hw.txt /freertr/everson/polka/rare/pra0101-sw.txt' ENTER;
tmux split-window -v -t 4 -p 50
tmux send 'java -jar /freertr/rtr.jar routersc /freertr/everson/polka/rare/mc36021-hw.txt /freertr/everson/polka/rare/mc36021-sw.txt' ENTER; 
tmux a;
