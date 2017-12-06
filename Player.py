##############################################
# Player | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################
from Song import Song
from Settings import *


class Player():
    def __init__(self, song):
        self.hitNotes = 0
        self.score = 0
        self.accuracy = 0
        self.song = song
        self.releasedNotes = 0
        self.notesList = song.notesList
        self.musicNotes = song.musicNotes

    def hitNote(self, note):
        for (i, testnote) in enumerate(self.notesList):
            if testnote == note:
                self.notesList.pop(i)
        self.score += 1

    def numReleasedNotes(self):
        threshold = WIDTH // 2
        for note in self.notesList:
            x = note.x
            if x < threshold:
                self.releasedNotes += 1

    def getTrebleNotes(self):
        return self.song.trebleNotes

    def getBassNotes(self):
        return self.song.bassNotes
