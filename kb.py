"""Instant input with keyboard"""
import sys
import termios
import tty
import os
import time
import platform
 

def getch():
    # Unix (Linux / macOS)
    if platform.system() in ['Linux','Darwin']:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
    
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    # Windows
    elif platform.system() in ['Windows']:
        fd = open(os.getcwd(),'rb').fileno
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
    
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    else:
        print("cant identify os status {}".format(platform.system()))


button_delay = 0.2
