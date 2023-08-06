__version__ = "1.4.0"

from . import _quietload    # disables pygame startup message

from pygame import Rect, Color, joystick
from . import time, digifont, emoji, data
from .common import Coord
from .music import music
from .game import Game
from .digifont import DigiText
from .perf import perf
from .constants import *

del _quietload
