##############################################
# MusicAnalyzer | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################

import Settings
import Note
import rtmidi

class Song():
    def __init__(self, notes, sig, tempo=120):
        self.notesList = notes
        self.timeSignature = sig
        self.tempo = tempo
