#!/usr/bin/env python3
from gpiozero import Button
from signal import pause
import os, sys

btn = Button(3, hold_time=3)
btn.when_held = lambda: os.system("poweroff")

pause()
