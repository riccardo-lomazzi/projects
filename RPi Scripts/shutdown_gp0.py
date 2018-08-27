#!/usr/bin/python
import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')
from gpiozero import Button
from subprocess import check_call
from signal import pause

def shutdown():
    check_call("poweroff", shell=True)

shutdown_btn = Button(3, hold_time=1)
shutdown_btn.when_held = shutdown

pause()