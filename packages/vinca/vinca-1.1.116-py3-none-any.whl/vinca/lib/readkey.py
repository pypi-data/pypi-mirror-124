# A simple module for reading a keystroke from the user
# adapted from the getchar function in the click library

import tty
import termios
import sys
import contextlib
import os
from types import SimpleNamespace

keys = SimpleNamespace(ESC = '\x1b', UP = '\x1b[A', DOWN = '\x1b[B', RIGHT = '\x1b[C',
			LEFT = '\x1b[D', BACK = '\x7f', CTRL_R = '\x12')

@contextlib.contextmanager
def raw_terminal():
	fd = sys.stdin.fileno()

	old_settings = termios.tcgetattr(fd) # save state of terminal

	try:
		tty.setraw(fd)
		yield fd
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		sys.stdout.flush() # restore state of terminal


def readkey():
	with raw_terminal() as fd:
		return os.read(fd, 4).decode()
