##############################################
# MusicAnalyzer | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################

import mido
import rtmidi
from mido import MidiFile
import Note
from Note import Notes
from Song import Song

filename = 'bach_minuet.mid'
mid = MidiFile('music/' + filename)
textOut = open('assets/' + filename.split('.')[0], 'w')


# port = mido.open_output()

def parseMIDI(file):
    # read midi file and filter notes
    song = []
    for msg in file:
        # print(msg)
        if isNote(msg):
            time = msg.time
            notes = msg.bytes()
            textOut.write(str(notes) + str(time) + '\n')
            song.append((notes, time))
    return song


def findTimeSignature(file):
    time = []
    for (i, msg) in enumerate(file):
        if isTimeSignature(msg):
            currTime = msg
            num, den = currTime.numerator, currTime.denominator
            time.append(([num, den], i))
    return time


def findTempo(file):
    for (i, msg) in enumerate(file):
        if isTempo(msg):
            tempo = msg.tempo
            return mido.tempo2bpm(tempo)


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


def getNotePairs(song):
    # find on/off note pairs
    notes = []
    pairs = []
    for elem in song:
        notes.append(elem[0])
    while len(notes) > 0:
        note_on = notes.pop(0)
        currNote = note_on[1]
        for i, elem in enumerate(notes):
            nextNote = elem[1]
            if nextNote == currNote:
                note_off = notes.pop(i)
                pairs.append((note_on, note_off))
                break
    return pairs


def midiPlayer():
    # makes a port to output midi files
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("Virtual output")
    return midiout


def closePlayer(player):
    del player


def extractNotes(noteList):
    # create note objects from song file
    noteObjects = []
    for data in noteList:
        note = data[0]
        dt = data[-1]  # delta time between notes
        channel = note[0]
        noteID = note[1]
        vel = note[2]
        # time.sleep(dt)
        Note.midiout.send_message(note)
        if not isNoteOff(note):
            noteObjects.append(Notes(noteID, vel, channel, dt))
    return noteObjects


def generateSong(mid):
    print('Song Name:', mid.tracks[0].name)
    print("Ticks:", mid.ticks_per_beat)
    song = parseMIDI(mid)
    print('Time:', mid.length)
    print('Bytes:', song, len(song))
    time_sig = findTimeSignature(mid)
    print('Time Signature:', time_sig)
    tempo = findTempo(mid)
    print('Tempo:', tempo)
    pairs = getNotePairs(song)
    print('Pairs:', pairs, len(pairs))
    output = extractNotes(song)
    print('Notes:', output, len(output))
    song = Song(output, time_sig, tempo)
    return song


song = generateSong(mid)

textOut.close()
