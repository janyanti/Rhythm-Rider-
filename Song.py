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
    noteDistance = {'eighth': STEP * 2 + NOTESTEP, 'quarter': STEP * 4,
                    'half': STEP * 6, 'whole': STEP * 12}

    def __init__(self, notes, sig, tempo=120):
        self.notesList = notes
        self.timeSignature = sig
        self.tempo = tempo
        self.startWidth = WIDTH + WIDTH // 2
        self.groups = self.groupNotes()
        self.musicNotes = self.generateNotes()
        self.trebleNotes, self.bassNotes = self.getClef()

    def generateNotes(self):
        result = []
        step = STEP * 3
        currWidth = self.startWidth
        for key in self.groups:
            for note in self.groups[key]:
                key = note.getType()
                step = Song.noteDistance[key]
                musicNote = MusicNote(currWidth, note)
                result.append(musicNote)
            currWidth += step
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

    def groupNotes(self):
        temp = self.notesList
        result = {}
        for elem in temp:
            pos = elem.getPosition()
            if not pos in result:
                result[pos] = [elem]
            else:
                result[pos].append(elem)
        return (result)
