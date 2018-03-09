#!/usr/bin/env python3
from gpiozero import LED
from signal import pause
import os, sys

led = LED(18)
led.blink(on_time=0.05, off_time=1)

pause()
