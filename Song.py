##############################################
# MusicAnalyzer | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################

from GameObjects import MusicNote
from Settings import *
from collections import Counter

##############################################
# Class
##############################################

class Song():
    noteDistance = {'16th': NOTESTEP * 3, 'eighth': STEP * 3, 'quarter': STEP * 6,
                    'half': STEP * 9, 'whole': STEP * 12}

    def __init__(self, name, notes, sig, PPQ, tempo=120):
        self.name = name
        self.notesList = notes
        self.timeSignature = sig
        self.tempo = tempo
        self.PPQ = PPQ
        self.noteVelocity = self.getVelocity()
        self.startWidth = WIDTH + WIDTH // 2
        self.groups = self.groupNotes()
        self.notePositions = self.positionNotes()
        print(self.notePositions)
        self.checkStem()
        self.musicNotes = self.generateNotes()
        self.trebleNotes, self.bassNotes = self.getClefs()

    def generateNotes(self):
        result = []
        mostCommon = self.mostCommon(self.notePositions)
        dx = self.noteVelocity
        currWidth = self.startWidth
        for (i, key) in enumerate(self.groups):
            for note in self.groups[key]:
                stem = self.stems[key]
                musicNote = MusicNote(stem, currWidth, note, dx)
                result.append(musicNote)
            if not self.notePositions[i] < 0.1:
                currWidth += (STEP * 6) * self.notePositions[i]
            else:
                currWidth += (STEP * 6) * mostCommon
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
        stem = {}
        for elem in temp:
            pos = elem.getPosition()
            if not pos in result:
                result[pos] = [elem]
            else:
                result[pos].append(elem)
        self.positionkeys = result.keys()
        print(result)
        return result

    def positionNotes(self):
        result = []
        data = sorted(self.positionkeys)
        ticks = (TICKS / (self.PPQ * self.tempo)) * (10 ** (-3))
        for i in range(len(data) - 1):
            x1 = data[i]
            x2 = data[i + 1]
            dist = x2 - x1
            deviation = round((dist / ticks) / self.PPQ, 2)
            result.append(deviation)
        result.append(0)
        return result

    def getVelocity(self):
        tempo = self.getTempo()
        dx = INTERCEPT + SLOPE * tempo
        return dx

    def checkStem(self):
        stems = {}
        for key in self.groups:
            note = self.groups[key][0]
            clef = note.getClef()
            noteID = note.noteID
            if clef is "Treble":
                if noteID >= 71:
                    stems[key] = 'down'
                else:
                    stems[key] = 'up'
            if clef is 'Bass':
                if noteID >= 50:
                    stems[key] = 'down'
                else:
                    stems[key] = 'up'
        print(stems)
        self.stems = stems

    def mostCommon(self, lst):
        data = Counter(lst)
        return max(lst, key=data.get)
