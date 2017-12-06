##############################################
# Game Sounds | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################

from Note import Notes
import random

##############################################
# Class Functions
##############################################

SOUNDINDEX = range(40, 100)


def buttonPress():
    choice = random.choice(SOUNDINDEX)
    Notes.playNote(Notes(choice))
