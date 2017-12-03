##############################################
# MusicAnalyzer | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################

from GameObjects import MusicNote
from Settings import *


##############################################
# Class
##############################################

class Song():
    noteDistance = {'16th': NOTESTEP * 3, 'eighth': STEP * 3, 'quarter': STEP * 6,
                    'half': STEP * 9, 'whole': STEP * 12}

    def __init__(self, notes, sig, tempo=120):
        self.notesList = notes
        self.timeSignature = sig
        self.tempo = tempo
        self.noteVelocity = self.getVelocity()
        self.startWidth = WIDTH + WIDTH // 2
        self.groups = self.groupNotes()
        self.musicNotes = self.generateNotes()
        self.trebleNotes, self.bassNotes = self.getClefs()

    def generateNotes(self):
        result = []
        dx = self.noteVelocity
        step = STEP * 3
        currWidth = self.startWidth
        for key in self.groups:
            steps = []
            for note in self.groups[key]:
                key = note.getType()
                steps.append(Song.noteDistance[key])
                musicNote = MusicNote(currWidth, note, dx)
                result.append(musicNote)
            currWidth += min(steps)
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

    def getClefs(self):
        treble, bass = [], []
        for note in self.musicNotes:
            if note.Note.getClef() == 'Treble':
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
        print(result)
        return result

    def getVelocity(self):
        tempo = self.getTempo()
        dx = INTERCEPT + SLOPE * tempo
        return dx
