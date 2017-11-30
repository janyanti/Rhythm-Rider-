##############################################
# Settings | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

import pygame as pg

# Game/Display
WIDTH = 1280
HEIGHT = 720
FPS = 50
TITLE = 'Rhythm Rider'

# Colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

# Game Constants
STEP = 30
NOTESTEP = STEP//2

# key inputs
ILLEGAL = [pg.K_LSHIFT, pg.K_RSHIFT, pg.K_INSERT]

# game modes
MODES = {'play': 'self.initGame()', 'select': 'self.initSelect',
         'help': 'self.initHelp', 'start': 'self.initStart'}

# music constants
TICKS = 60000
INTERCEPT = 1.6
SLOPE = 0.0335

# grpahics
SFY = 590
SFDX = 280
