##############################################
# Settings | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################


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
PORTAL = range(360, 440)

# key inputs

# game modes
MODES = {'play': 'self.initGame()\nself.gameOver = False', 'select': 'self.initSelect()',
         'help': 'self.initHelp()', 'start': 'self.initStart()',
         'options': 'self.initOptions()'}

CPU = '''self.hasCPU = True \nself.pianoOn = False\nself.hasDual = False'''
SINGLE = '''self.hasCPU = False \nself.pianoOn = False\nself.hasDual = False'''
PIANO = '''self.hasCPU = True \nself.pianoOn = True\nself.hasDual = False'''
DUAL = '''self.hasCPU = True \nself.pianoOn = False\nself.hasDual = True'''

TREBLE = 'self.gameMode = "treble"'
BASS = 'self.gameMode = "bass"'

INPUTS = {'cpumode': CPU, 'dualmode': DUAL, 'singlemode': SINGLE, 'pianomode': PIANO}
NOTESMODE = {'trebleplay': TREBLE, 'bassplay': BASS}

GAMEOVER = {'retry': 'game', 'newsong': 'select', 'mainmenu': 'start'}


# music constants
TICKS = 60000
INTERCEPT = 1.6
SLOPE = 0.0335

# grpahics
SFY = 590  # Song File Y-pos
SFDX = 280  # change in x
IMX = 970  # Input mode X-pos
IMDY = 156  # cgange in y
