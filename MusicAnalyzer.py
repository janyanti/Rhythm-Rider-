##############################################
# MusicAnalyzer | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################

import copy
import sys
import mido
from mido import MidiFile
from Note import Notes
from Settings import *
from Song import Song

# move this to generate song method with filename as argument
filename = 'ode_to_joy.mid'
mid = MidiFile('music/' + filename)
textOut = open('assets/' + filename.split('.')[0], 'w')


##############################################
# Class Functions
##############################################

def parseMIDI(file):
    # read midi file and filter notes
    time = 0
    song = []
    for msg in file:
        # print(msg)
        if isNote(msg):
            time += msg.time
            notes = msg.bytes()
            textOut.write(str(notes) + str(round(time, 2)) + '\n')
            song.append([notes, formatTime(time)])
    return song


def findTimeSignature(file):
    # get the numerator and denominator of time signature
    time = []
    for (i, msg) in enumerate(file):
        if isTimeSignature(msg):
            currTime = msg
            num, den = currTime.numerator, currTime.denominator
            time.append(([num, den], i))
    return time


def findTempo(file):
    # returns tempo of song
    count = 0
    for (i, msg) in enumerate(file):
        if isTempo(msg):
            tempo = msg.tempo
            count += 1
            break
    if not count == 0:
        return int(mido.tempo2bpm(tempo))
    else:
        return 120


def isTimeSignature(msg):
    return msg.type == 'time_signature'


def isTempo(msg):
    return msg.type == 'set_tempo'


def isNote(msg):
    # check if meta message denotes note played
    msgType = msg.type
    return 'note_on' == msgType or 'note_off' == msgType


def isNoteOff(msg):
    # filter out 'note_off' messages
    channel, velocity = msg[0], msg[-1]
    return channel < 144 or velocity == 0


def formatTime(time):
    data = '{0}'.format(round(time, 2))
    return float(data)


def getNotePairs(song):
    # find on/off note pairs with note durations
    notes = copy.deepcopy(song)
    pairs = []
    while len(notes) > 0:
        data = notes.pop(0)
        note_on = data[0]
        startTime = data[-1]
        currNote = note_on[1]
        for i, elem in enumerate(notes):
            data = notes[i]
            note_off = data[0]
            nextNote = note_off[1]
            endTime = data[-1]
            if nextNote == currNote:
                notes.pop(i)
                pairs.append((note_on, endTime - startTime))
                break
    return pairs


def compoundNotePairs(song, pairs, PPQ, BPM):
    noteOn = []
    result = []
    for data in song:
        note = data[0]
        if not isNoteOff(note):
            noteOn.append(data)
    for (i, pair) in enumerate(pairs):
        note = noteOn[i][0]
        pos = noteOn[i][-1]
        dt = pair[-1]
        type = extractNoteType(PPQ, BPM, dt)
        result.append((note, pos, type))
    return result


def extractNotes(noteList):
    # create note objects from song file
    noteObjects = []
    for data in noteList:
        note, pos, type = data
        # note = data[0]
        # dt = data[-1]  # delta time between notes
        channel = note[0]
        noteID = note[1]
        vel = note[2]
        # time.sleep(dt)
        # Note.midiout.send_message(note)
        if not isNoteOff(note):
            noteObjects.append(Notes(noteID, vel, channel, pos, type))
    return noteObjects


def extractNoteType(PPQ, BPM, dt):
    noteType = {0.5: 'eighth', 1: 'quarter', 2: 'half', 4: 'whole'}
    ticks = (TICKS / (PPQ * BPM)) * (10 ** (-3))
    notePPQ = dt / ticks
    comp = notePPQ / PPQ
    currType = ''
    leastDist = sys.maxsize
    for key in noteType:
        dist = abs(key - comp)
        if dist < leastDist:
            currType = noteType[key]
            leastDist = dist
    return currType


def generateSong(mid):
    print('Song Name:', mid.tracks[0].name)
    print("Ticks:", mid.ticks_per_beat)
    PPQ = mid.ticks_per_beat
    song = parseMIDI(mid)
    print('Time:', mid.length)
    # print('Bytes:', song, len(song))
    timeSig = findTimeSignature(mid)
    # print('Time Signature:', time_sig)
    BPM = findTempo(mid)
    print('Tempo:', BPM)
    pairs = getNotePairs(song)
    print('Pairs:', pairs, len(pairs))
    compound = compoundNotePairs(song, pairs, PPQ, BPM)
    print('Compound:', compound, len(compound))
    output = extractNotes(compound)
    print('Notes:', output, len(output))

    result = Song(output, timeSig, BPM)
    return result


song = generateSong(mid)

textOut.close()
