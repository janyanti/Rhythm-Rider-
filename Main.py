##############################################
# Main | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################
import os
import pygame.midi
import MusicAnalyzer
import time
import GameObjects
from Player import Player
from Settings import *
from Note import Notes
import pygame
from pygame.locals import *
from collections import deque
import tkinter
from tkinter import filedialog

import threading


os.environ['SDL_VIDEO_CENTERED'] = '1'


class Game(object):
    def init(self):
        self.modes = MODES
        self.mode = 'start'
        self.pianoOn = False
        self.filename = 'music/fur_elise.mid'
        self.timer = 0
        self.noteQ = deque()
        self.NoteFont = pygame.font.SysFont('alba', 100)
        self.GameFont = pygame.font.SysFont('alba', 35)
        self.FileFont = pygame.font.SysFont('agency fb', 45)
        self.timeFont = pygame.font.Font('assets/Aruvarb.ttf', 116)
        self.inputText = ''
        self.gameMode = 'bass'
        self.hasCPU = True
        self.isPaused = False

        # start screen
        self.initStart()
        self.initSelect()


        # help screen
        # helpSprite = pygame.sprite.Sprite()
        # helpSprite.image = pygame.image.load('assets/helpscreen.png')
        # helpSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        # self.helpscreen = pygame.sprite.Group(helpSprite)

    def mousePressed(self, x, y):
        if not self.mode == 'play':
            self.onClick(x, y)

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        startHero = self.getStartHero()
        startHero.y = y
        startHero.x = x

    def mouseDrag(self, x, y):
        pass

    def initStart(self):
        # create starting conditions
        startSprite = pygame.sprite.Sprite()
        startSprite.image = pygame.image.load('assets/startscreen.png')
        startSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.startScreen = pygame.sprite.Group(startSprite)
        self.startHero = pygame.sprite.Group(GameObjects.startHero())
        self.spawnedNotes = pygame.sprite.Group()
        play = GameObjects.Button(640, 540, 'select')
        help = GameObjects.Button(640, 650, 'help')
        options = GameObjects.Button(1100, 665, 'options')
        print(options.rect, help.rect)
        self.startButtons = pygame.sprite.Group(play, help, options)

    def initSelect(self):
        # define screen/attributes for this mode
        selectSprite = pygame.sprite.Sprite()
        selectSprite.image = GameObjects.load_images('selectscreen')
        selectSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.selectScreen = pygame.sprite.Group(selectSprite)
        self.songFiles = pygame.sprite.Group(self.generateSongFiles())

    def initOptions(self):
        optionsSprite = pygame.sprite.Sprite()
        optionsSprite.image = GameObjects.load_images('optionsscreen')
        optionsSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.optionsScreen = pygame.sprite.Group(optionsSprite)
        self.InputModes = pygame.sprite.Group(self.generateInputModes())
        self.NotesModes = pygame.sprite.Group(self.generateNotesModes())

    def selectMode(self, mode):
        command = self.modes[mode]
        print(command)
        eval(command)
        self.mode = mode

    def initGame(self):
        self.player = Player(MusicAnalyzer.generateSong(self.filename))
        clefs = (GameObjects.TrebleClef(90, 186), GameObjects.BassClef(90, 504))
        self.Lines = pygame.sprite.Group(GameObjects.Lines.generateStaff())
        self.Clefs = pygame.sprite.Group(clefs)
        self.Notes = pygame.sprite.Group(self.player.musicNotes)
        self.Hero = pygame.sprite.Group(GameObjects.Hero(y=135))
        if self.gameMode == 'treble':
            self.targetNotes = self.player.getTrebleNotes()
            self.CPUTargets = self.player.getBassNotes()
            cpuHeight = 540
        else:
            self.getHero().y = 540
            self.targetNotes = self.player.getBassNotes()
            self.CPUTargets = self.player.getTrebleNotes()
            cpuHeight = 135
        if self.hasCPU:
            self.CPU = pygame.sprite.Group(GameObjects.Hero(y=cpuHeight))
            self.moveCPU()
        self.total = len(self.targetNotes)
        self.splitNote(self.targetNotes.pop(0))
        self.numerator, self.denominator = self.player.song.getTimeSignature()


    def splitNote(self, note):
        self.currNote = note.getNoteName()
        self.currOctave = note.getOctave()

    def keyPressed(self, keyCode, modifier):
        if self.mode == 'play':
            hero = self.getHero()
            if keyCode == pygame.K_UP:
                hero.changeDirection(-1)
                hero.move(WIDTH, HEIGHT)
            if keyCode == pygame.K_DOWN:
                hero.changeDirection(1)
                hero.move(WIDTH, HEIGHT)
            if keyCode == pygame.K_p:
                self.isPaused = not self.isPaused
        if self.mode == 'select':
            self.keySelect(keyCode)
        if self.mode == 'options':
            if keyCode == pygame.K_RETURN:
                self.mode = 'start'

    def keySelect(self, keyCode):
        root = tkinter.Tk()
        root.withdraw()
        if keyCode == pygame.K_BACKSPACE:
            file_path = filedialog.askopenfilename()
            self.inputText = str(file_path)
        else:
            time.sleep(0.5)
            if not self.inputText == '' and self.checkFilePath(self.inputText):
                self.filename = self.inputText
            self.selectMode('play')


    def keyReleased(self, keyCode, modifier):
        pass

    def keyToNote(self, data):
        # takes in keyboard input
        data = data[0][0][:-1]
        if data[-1] == 0:
            data.append(0)
            note = Notes.toNote(data)
            self.noteQ.append(note)

    def inputNote(self):
        try:
            result = self.noteQ.popleft()
            print(result)
        except:
            return

    def timerFired(self, dt):
        self.timer += 1
        self.inputNote()
        if self.mode == 'start':
            self.startHero.update()
        if self.timer % 10 == 0:
            spawn = self.getStartHero().spawnNote()
            self.spawnedNotes.add(spawn)
        self.spawnedNotes.update()
        if not self.isPaused:
            if self.mode == 'play':
                self.Notes.update()
                self.Hero.update()
                if self.hasCPU:
                    self.CPU.update()
                self.clefCollision()
                self.noteCollision()
        if self.mode == 'select':
            pass

    def redrawAll(self, screen):
        if self.mode == 'start':
            self.drawStart(screen)
        elif self.mode == 'play':
            self.drawGame(screen)
        elif self.mode == 'select':
            self.drawSelect(screen)
        elif self.mode == 'options':
            self.drawOptions(screen)

    def drawStart(self, screen):
        self.startScreen.draw(screen)
        self.spawnedNotes.draw(screen)
        self.startButtons.draw(screen)
        self.startHero.draw(screen)

    def drawSelect(self, screen):
        self.selectScreen.draw(screen)
        self.songFiles.draw(screen)
        file = self.FileFont.render(self.inputText, True, BLACK, None)
        screen.blit(file, (STEP * 3, 285))

    def drawOptions(self, screen):
        self.optionsScreen.draw(screen)
        self.InputModes.draw(screen)
        self.NotesModes.draw(screen)

    def generateSongFiles(self):
        x = 200
        songFiles = []
        for i in range(len(GameObjects.SongFile.songs)):
            song = GameObjects.SongFile(x, SFY, i)
            songFiles.append(song)
            x += SFDX
        return songFiles

    def generateInputModes(self):
        y = 210
        modesList = []
        for i in range(len(GameObjects.InputModes.modes)):
            mode = GameObjects.InputModes(IMX, y, i)
            modesList.append(mode)
            y += IMDY
        return modesList

    def generateNotesModes(self):
        y = 250
        notesList = []
        for i in range(len(GameObjects.NotesModes.modes)):
            mode = GameObjects.NotesModes(315, y, i)
            notesList.append(mode)
            y += 300
        return notesList

    def drawGame(self, screen):
        for line in self.Lines:
            line.draw(screen)
        self.Clefs.draw(screen)
        for note in self.Notes:
            note.draw(screen)
        self.Hero.draw(screen)
        if self.hasCPU:
            self.CPU.draw(screen)
        self.drawNextText(screen)
        self.drawTimeSignature(screen)
        self.drawTempo(screen)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def getHero(self):
        result = None
        for hero in self.Hero:
            result = hero
        return result

    def getCPU(self):
        result = None
        for hero in self.CPU:
            result = hero
        return result

    def getStartHero(self):
        result = None
        for hero in self.startHero:
            result = hero
        return result

    def onClick(self, x, y):
        if self.mode == 'select':
            self.clickSelect(x, y)
        if self.mode == 'start':
            self.clickStart(x, y)
        if self.mode == 'options':
            self.clickModes(x, y)

    def clickModes(self, x, y):
        for mode in self.InputModes:
            key = mode.name
            if self.pointCollision(mode, x, y):
                mode.click()
                exec(INPUTS[key])
        for clef in self.NotesModes:
            key = clef.name
            if self.pointCollision(clef, x, y):
                clef.click()
                exec(NOTESMODE[key])

    def clickSelect(self, x, y):
        for songFile in self.songFiles:
            if self.pointCollision(songFile, x, y):
                songFile.click()
                self.filename = songFile.id

    def clickStart(self, x, y):
        for button in self.startButtons:
            if self.pointCollision(button, x, y):
                mode = button.name
                self.selectMode(mode)

    def pointCollision(self, obj, x, y):
        x1, y1, w, h = obj.x, obj.y, obj.width, obj.height
        xPos = set(range(x1 - w, x1 + w))
        yPos = set(range(y1 - h, y1 + h))
        if x in xPos and y in yPos:
            return True
        return False


    def checkFilePath(self, path):
        return not os.path.isdir(path) and os.path.isfile(path)

    def drawSurface(self, songFile):
        x, y, w, h = songFile.getRect()
        position = x, y
        size = w, h
        rect = pygame.Rect(position, size)
        image = pygame.Surface(size)
        pygame.draw.rect(image, GREEN, rect)

    def drawNextText(self, screen):
        note = self.NoteFont.render(str(self.currNote), True, BLACK)
        screen.blit(note, (WIDTH // 2, HEIGHT // 2 - STEP * 3))
        octave = self.GameFont.render(str(self.currOctave), True, BLACK)
        screen.blit(octave, (WIDTH // 2 + STEP * 4, HEIGHT // 2 + STEP))
        acc = "Accuracy: %.2f" % (self.player.accuracy) + '%'
        accuracy = self.GameFont.render(acc, True, BLACK)
        screen.blit(accuracy, (WIDTH - 10 * STEP, NOTESTEP * 2))

    def drawTimeSignature(self, screen):
        numer = self.timeFont.render(str(self.numerator), True, BLACK)
        denom = self.timeFont.render(str(self.denominator), True, BLACK)
        screen.blit(numer, (STEP * 6, -NOTESTEP * 5))
        screen.blit(denom, (STEP * 6, -NOTESTEP))
        screen.blit(numer, (STEP * 6, NOTESTEP * 17))
        screen.blit(denom, (STEP * 6, NOTESTEP * 21))

    def drawTempo(self, screen):
        tempo = self.player.song.getTempo()
        text = 'Tempo = %d BPM' % tempo
        result = self.GameFont.render(text, True, BLACK)
        screen.blit(result, (6 * STEP, NOTESTEP * 2))


    def clefCollision(self):
        # checks for specific note
        for musicNote in self.Notes:
            if pygame.sprite.spritecollide(musicNote, self.Clefs, False):
                note = musicNote.Note
                musicNote.kill()
                self.player.missedNotes += 1
                self.player.notesList.remove(note)
                break
                # self.splitNote(self.player.notesList[0])

    def noteCollision(self):
        try:
            for musicNote in self.Notes:
                if pygame.sprite.collide_circle(musicNote, self.getHero()):
                    note = musicNote.Note
                    musicNote.Note.playNote()
                    musicNote.kill()
                    self.player.hitNote(musicNote)
                    self.player.notesList.remove(note)
                    self.splitNote(self.targetNotes.pop(0))
                    self.player.accuracy = ((self.player.score / self.total * 100))
            if self.hasCPU:
                self.cpuCollision()
        except:
            pass

    def cpuCollision(self):
        for note in self.Notes:
            if pygame.sprite.spritecollide(note, self.CPU, False):
                note.Note.playNote()
                self.cpuHit(note)
                note.kill()
                self.moveCPU()

    def moveCPU(self):
        if not self.CPUTargets == []:
            target = self.CPUTargets.pop(0)
            height = target.getHeight()
            self.getCPU().cpuMove(height)

    def cpuHit(self, note):
        for (i, testnote) in enumerate(self.CPUTargets):
            if testnote == note:
                self.CPUTargets.pop(i)

    def __init__(self, w=WIDTH, h=HEIGHT, f=FPS, t=TITLE):
        self.width = w
        self.height = h
        self.fps = f
        self.title = t
        self.bgColor = WHITE
        pygame.init()
        pygame.midi.init()

    def run(self):

        clock = pygame.time.Clock()
        flags = DOUBLEBUF
        screen = pygame.display.set_mode((self.width, self.height), flags)
        screen.set_alpha(None)
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        self.screen = screen
        # self.inp = pygame.midi.Input(1)
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            # if self.inp.poll() and self.pianoOn:
            #     # no way to find number of messages in queue
            #     data = self.inp.read(1000)
            #     self.keyToNote(data)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                              event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                              event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
