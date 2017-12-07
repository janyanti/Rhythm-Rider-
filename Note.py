##############################################
# Notes | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################
import os
import time
import rtmidi
from Settings import *
import math
import string

##############################################
# Class Functions
##############################################

# makes a port to output midi files
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")


def digitToNotes():
    # maps notes to octaves
    result = []
    notes = ['C', 'C#', 'D', 'D#', 'E',
             'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    for i in range(-2, 9):
        for note in notes:
            octNote = note + str(i)
            result.append(octNote)

    return result


def notesLadder():
    # plays all notes in range
    channel, velocity = 144, 112
    for i in range(len(digitToNotes())):
        noteID = i
        note = Notes(noteID, velocity, channel)
        note.playNote()



def listToDict(list):
    # turn list into dictionary with indexes as keys
    result = dict()
    for i, elem in enumerate(list):
        result[i] = elem
    return result


##############################################
# Classes
##############################################

class Notes():
    # music note object
    noteConvert = listToDict(digitToNotes())
    clefs = ['Bass', 'Treble']

    def __init__(self, ID, vel=112, chan=144, dt=0, typ='quarter'):
        self.noteID = ID
        self.velocity = vel
        self.channel = chan
        self.dt = dt
        self.type = typ
        self.note = Notes.noteConvert[ID]
        self.clef = self.getClef()
        self.hasCross()

    def __repr__(self):
        return str(self.note)

    def __eq__(self, other):
        return isinstance(other, Notes) and self.getHashables() == other.getHashables()

    def __hash__(self):
        return hash(self.getHashables())

    def getHashables(self):
        return (self.noteID)

    def playNote(self):
        note = [self.channel, self.noteID, self.velocity]
        midiout.send_message(note)
        # time.sleep(0.5)
        # note[-1] = 0
        # midiout.send_message(note)

    def getClef(self):
        # returns clef classification of note
        if self.noteID >= 60:
            return Notes.clefs[-1]
        return Notes.clefs[0]

    def getPosition(self):
        return self.dt

    def getNoteName(self):
        name = list(self.note)
        for char in name:
            if char in string.digits or char is '-':
                name.remove(char)
        name = ''.join(name)
        return name

    def getOctave(self):
        # returns octave of note
        parse = self.note
        n = list(parse)
        if '-' in n:
            scale = -1
        else:
            scale = 1
        num = int(n[-1])
        return num * scale

    def getHeight(self):
        # returns position of note based on real music notation
        pos = None
        clef = self.getClef()
        note = self.getBaseNote()
        if clef is 'Treble':
            noteRef = Notes(60)
            dist = math.ceil((note.noteID - noteRef.noteID) / 2)
            pos = 270 - dist * NOTESTEP
        elif clef is 'Bass':
            noteRef = Notes(36)
            dist = math.ceil((note.noteID - noteRef.noteID) / 2)
            pos = 615 - (dist) * NOTESTEP
        return pos

    def getBaseNote(self):
        noteID = self.noteID
        if self.isAccidental():
            return Notes(noteID - 1, self.velocity, self.channel, self.dt)
        return self

    def getType(self):
        return self.type

    def isAccidental(self):
        note = self.note
        return "#" in note

    @staticmethod
    def toNote(list):
        # creates a note object from list
        channel, noteID, velocity, dt = tuple(list)
        # channel = list.pop(0)
        # noteID = list.pop(0)
        # velocity = list.pop(0)
        # dt = list.pop()
        result = Notes(noteID, velocity, channel, dt)
        return result

    def hasCross(self):
        ID = self.noteID
        if ID in CROSSES:
            self.cross = True
        else:
            self.cross = False

# l = [144, 60, 112, 0]
# c = Notes.toNote(l)
# print(c.getHeight())
