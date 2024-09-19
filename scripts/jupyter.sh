#!/usr/bin/env bash
CMD="cd /home/norlab/glo4001 && source venv/bin/activate && jupyter notebook --allow-root"
screen -S jupyter -d -m bash -c "$CMD"
screen -r jupyter
