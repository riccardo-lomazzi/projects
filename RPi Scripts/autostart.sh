#!/bin/bash
python /storage/.config/scripts/shutdown.py &

#structure: ( *command*, *command* ) &
#command: (Python) --> python *path* OR (SH) --> sh *path*

#place this file in /storage/.config and scripts in /storage/.config/scripts
#if it doesn't work, try "sh *path to autostart.sh*" to see what happens when called
#also, try to execute the single scripts