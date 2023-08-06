# -*- coding: utf-8 -*-

__version__ = "0.0.40"
__author__ = "BriFuture"

"""
0.0.40: move socket server and bluetooth into network, remove _globals

0.0.35: optimize scripts in torch folder

0.0.34: fix database error

0.0.33: move logger from utils to avoid log too much content

0.0.32: update with pyupdator

0.0.22: socket server has been improved a lot, interface has changed

0.0.17: scripts in `myscripts` folder could add more scripts
without change main.py file.
"""

from .utils import createLogger, initGetText
from ._constants import BFF_ROOT_PATH, BFF_OTHER_PATH


#Dictionary with console color codes to print text
terminal_colors = {
    'HEADER' : "\033[95m",
    'OKBLUE' : "\033[94m",
    'RED' : "\033[91m",
    'OKYELLOW' : "\033[93m",
    'GREEN' : "\033[92m",
    'LIGHTBLUE' : "\033[96m",
    'WARNING' : "\033[93m",
    'FAIL' : "\033[91m",
    'ENDC' : "\033[0m",
    'BOLD' : "\033[1m",
    'UNDERLINE' : "\033[4m" 
}