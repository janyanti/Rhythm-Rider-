##############################################
# MusicAnalyzer | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################

from Settings import *
import Note
from GameObjects import MusicNote
import rtmidi

class Song():
    def __init__(self, notes, sig, tempo=120):
        self.notesList = notes
        self.timeSignature = sig
        self.tempo = tempo
        self.startWidth = WIDTH + WIDTH // 2
        self.musicNotes = self.generateNotes()
        self.trebleNotes, self.bassNotes = self.getClef()

    def generateNotes(self):
        result = []
        currWidth = self.startWidth
        for note in self.notesList:
            musicNote = MusicNote(currWidth, note)
            result.append(musicNote)
            currWidth += STEP * 3
        return result

    def getTimeSignature(self):
        self.timeSignature = self.timeSignature[-1]
        sig = self.timeSignature[0]
        num, den = tuple(sig)
        return (num, den)

    def getClef(self):
        treble, bass = [], []
        for note in self.notesList:
            if note.getClef() == 'Treble':
                treble.append(note)
            else:
                bass.append(note)
        return treble, bass

    def getTempo(self):
        return int(self.tempo)
