import multiprocessing
from Note import Notes
import queue
import time
import MIDIInput
# import Main
import threading

stack = queue.Queue()
result = []


def getNote():
    print('Hi')
    try:
        note = MIDIInput.getMessage()
        stack.put(note)
    except:
        print('No input')


def printNote():
    try:
        result = stack.get()
        print(result)
    except:
        print(None)
        return


if __name__ == '__main__':

    getNote = multiprocessing.Process(target=getNote())
    playNote = multiprocessing.Process(target=printNote())
    start = time.time()
    while True:
        getNote.start()
        getNote.join()
        playNote.start()

    end = time.time()
    print(end - start)
