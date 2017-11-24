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


def getPlayer():
    # makes a port to output midi files
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")
    return midiout


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
    Clefs = ['Bass', 'Treble']

    def __init__(self, noteID, velocity=112, channel=144, dt=0):
        self.noteID = noteID
        self.velocity = velocity
        self.channel = channel
        self.dt = dt
        self.note = Notes.noteConvert[noteID]
        self.type = self.getClef()

    def __repr__(self):
        return str(self.note)

    def playNote(self):
        note = [self.channel, self.noteID, self.velocity]
        player = getPlayer()
        player.send_message(note)
        time.sleep(0.75)
        note[-1] = 0
        player.send_message(note)

    def getClef(self):
        # returns clef classification of note
        if self.noteID >= 60:
            return Notes.Clefs[-1]
        return Notes.Clefs[0]

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
        print(self)
        note = self.getBaseNote()
        print(note)
        if clef is 'Treble':
            noteRef = Notes(60)
            dist = math.ceil((note.noteID - noteRef.noteID) / 2)
            print(dist)
            pos = 270 - dist * NOTESTEP
        elif clef is 'Bass':
            noteRef = Notes(36)
            dist = math.ceil((note.noteID - noteRef.noteID) / 2)
            print(dist)
            pos = 605 - (dist) * NOTESTEP
        return pos

    def getBaseNote(self):
        noteID = self.noteID
        if self.isAccidental():
            return Notes(noteID - 1, self.velocity, self.channel, self.dt)
        return self

    def isAccidental(self):
        note = self.note
        return "#" in note

    @staticmethod
    def toNote(list):
        # creates a note object from list
        channel = list.pop(0)
        noteID = list.pop(0)
        velocity = list.pop(0)
        dt = list.pop()
        result = Notes(noteID, velocity, channel, dt)
        return result
