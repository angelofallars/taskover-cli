"""Instant input with keyboard"""
import sys
import termios
import tty
import os
import time
 

def getch():
    # Unix (Linux / macOS)
    if os.name != "nt":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
    
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    # Windows
    else:
        # TODO: !!! Add the Windows-specific code here !!!
        pass


button_delay = 0.2
