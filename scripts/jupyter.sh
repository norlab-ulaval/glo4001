#!/usr/bin/env bash
cd /home/norlab/glo4001/scripts || exit
#./shutdown_jupyter.sh
cd /home/norlab/glo4001 || exit
source venv/bin/activate
jupyter notebook --allow-root
