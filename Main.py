##############################################
# Main | 15-112 Term Project
# Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################
import os
import time
import tkinter
from collections import deque
from tkinter import filedialog

import pygame
import pygame.midi
from pygame.locals import *

import GameObjects
import MusicAnalyzer
from Note import Notes
from GameSounds import *
from Player import Player
from Settings import *

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Game(object):
    def init(self):
        self.mode = 'start'
        self.pianoOn = False
        self.gameOver = False
        self.hasDual = False
        self.filename = 'music/fur_elise.mid'
        self.timer = 0
        self.noteQ = deque(maxlen=5)
        self.NoteFont = pygame.font.SysFont('alba', 80)
        self.GameFont = pygame.font.SysFont('alba', 35)
        self.GameOverFont = pygame.font.SysFont('alba', 38)
        self.FileFont = pygame.font.SysFont('agency fb', 45)
        self.timeFont = pygame.font.Font('assets/Aruvarb.ttf', 116)
        self.gameMode = 'treble'
        self.inputText = ''
        self.backarrow = pygame.sprite.Group(GameObjects.Button(60, 34, 'backarrow'))
        self.hasCPU = True
        self.isPaused = False

        # start screen
        self.initStart()
        self.initSelect()

    def mousePressed(self, x, y):
        # if not self.mode == 'play':
        self.onClick(x, y)

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        if not self.mode == 'play':
            try:
                startHero = self.getStartHero()
                startHero.y = y
                startHero.x = x
            except:
                pass

    def mouseDrag(self, x, y):
        pass

    def initStart(self):
        # create starting conditions
        startSprite = pygame.sprite.Sprite()
        startSprite.image = GameObjects.load_images('startscreen')
        startSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.startScreen = pygame.sprite.Group(startSprite)
        self.startHero = pygame.sprite.Group(GameObjects.startHero())
        self.spawnedNotes = pygame.sprite.Group()
        play = GameObjects.Button(640, 540, 'select')
        help = GameObjects.Button(640, 650, 'help')
        options = GameObjects.Button(1100, 665, 'options')
        self.startButtons = pygame.sprite.Group(play, help, options)

    def initHelp(self):
        self.helpIndex = 0
        helpSprite = pygame.sprite.Sprite()
        self.pageList = ['helpscreen', 'helpscreen1']
        helpSprite.image = GameObjects.load_images(self.pageList[self.helpIndex])
        helpSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.helpscreen = pygame.sprite.Group(helpSprite)
        next = GameObjects.Button(1160, 680, 'next')
        back = GameObjects.Button(120, 680, 'back')
        self.nextButton = pygame.sprite.Group(next)
        self.backButton = pygame.sprite.Group(back)

    def initSelect(self):
        # define screen/attributes for this song selection
        selectSprite = pygame.sprite.Sprite()
        selectSprite.image = GameObjects.load_images('selectscreen')
        selectSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.selectScreen = pygame.sprite.Group(selectSprite)
        self.songFiles = pygame.sprite.Group(self.generateSongFiles())
        self.currNote, self.currOctave = 'C', '3'

    def initOptions(self):
        # define graphics/functions for options menu
        optionsSprite = pygame.sprite.Sprite()
        optionsSprite.image = GameObjects.load_images('optionsscreen')
        optionsSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.optionsScreen = pygame.sprite.Group(optionsSprite)
        self.InputModes = pygame.sprite.Group(self.generateInputModes())
        self.NotesModes = pygame.sprite.Group(self.generateNotesModes())

    def selectMode(self, mode):
        # select game mode
        command = MODES[mode]
        exec(command)
        self.mode = mode

    def initGameOver(self):
        gameOverMenu = pygame.sprite.Sprite()
        gameOverMenu.image = GameObjects.load_images('gameover')
        gameOverMenu.rect = pygame.Rect((410, 238), (460, 245))
        self.gameOverMenu = pygame.sprite.Group(gameOverMenu)
        retryButton = GameObjects.Button(648, 425, 'retry')
        MMButton = GameObjects.Button(790, 425, 'mainmenu')
        newSongButton = GameObjects.Button(484, 425, 'newsong')
        self.gameOverButtons = pygame.sprite.Group([retryButton, MMButton, newSongButton])

    def initGame(self):
        self.initGameOver()
        self.player = Player(MusicAnalyzer.generateSong(self.filename))
        clefs = (GameObjects.TrebleClef(90, 186), GameObjects.BassClef(90, 504))
        self.Lines = pygame.sprite.Group(GameObjects.Lines.generateStaff())
        self.Clefs = pygame.sprite.Group(clefs)
        self.Notes = pygame.sprite.Group(self.player.musicNotes)
        self.Treble = pygame.sprite.Group(self.player.getTrebleNotes())
        self.Bass = pygame.sprite.Group(self.player.getBassNotes())
        self.Hero = pygame.sprite.Group(GameObjects.Hero(y=135))
        self.heroSpawn = pygame.sprite.Group()
        if self.gameMode == 'treble':
            self.targetNotes = self.Treble
            self.CPUTargets = self.Bass
            self.Portal = pygame.sprite.Group(GameObjects.NotePortal(180))
            cpuHeight = 540
        else:
            self.getHero().y = 540
            self.targetNotes = self.Bass
            self.CPUTargets = self.Treble
            self.Portal = pygame.sprite.Group(GameObjects.NotePortal(495))
            cpuHeight = 135
        if self.hasCPU:
            self.CPU = pygame.sprite.Group(GameObjects.Hero(y=cpuHeight))
            self.getNextCPU()
            self.moveCPU()
        self.total = len(self.player.notesList)
        self.pianoTargets = None
        self.getNextTarget()

        self.numerator, self.denominator = self.player.song.getTimeSignature()

    def splitNote(self, notes):
        names = []
        if len(notes) <= 1:
            self.currNote = notes[0].Note.getNoteName()
            self.currOctave = notes[0].Note.getOctave()
        else:
            for note in notes:
                name = note.Note.getNoteName()
                names.append(name)
            self.currNote = ' '.join(names)
            self.currOctave = ''

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_p:
            self.isPaused = not self.isPaused
        if self.mode == 'play' and not self.pianoOn:
            hero = self.getHero()
            if keyCode == pygame.K_UP:
                hero.changeDirection(-1)
                hero.move(WIDTH, HEIGHT)
            if keyCode == pygame.K_DOWN:
                hero.changeDirection(1)
                hero.move(WIDTH, HEIGHT)
            if keyCode == pygame.K_w and self.hasDual:
                cpu = self.getCPU()
                cpu.changeDirection(-1)
                cpu.move(WIDTH, HEIGHT)
            if keyCode == pygame.K_s and self.hasDual:
                cpu = self.getCPU()
                cpu.changeDirection(1)
                cpu.move(WIDTH, HEIGHT)
        if self.mode == 'select':
            self.keySelect(keyCode)
        if self.mode == 'options':
            if keyCode == pygame.K_RETURN:
                self.mode = 'start'
        if self.mode == 'help':
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
        targets = [elem.Note for elem in self.pianoTargets]
        try:
            result = self.noteQ.popleft()
            print(result)
            for note in targets:
                if result == note:
                    note.playNote()
            return True
        except:
            return False

    def timerFired(self, dt):
        self.timer += 1
        if self.mode == 'start':
            self.startHero.update()
            if self.timer % 10 == 0:
                try:
                    spawn = self.getStartHero().spawnNote()
                    self.spawnedNotes.add(spawn)
                except:
                    pass
            self.spawnedNotes.update()
        if not self.isPaused:
            if self.mode == 'play':
                self.Notes.update()
                self.Hero.update()
                if self.timer % 10 == 0:
                    spawn = self.getHero().spawnNote()
                    self.heroSpawn.add(spawn)
                if not self.pianoOn:
                    self.heroSpawn.update()
                if self.hasCPU:
                    self.getNextCPU()
                    self.CPU.update()
                self.getNextTarget()
                self.clefCollision()
                self.noteCollision()
                self.checkGameStatus()
                self.checkLostNotes()
        if self.mode == 'select':
            pass

    def redrawAll(self, screen):
        if self.mode == 'start':
            self.drawStart(screen)
        elif self.mode == 'play':
            self.drawGame(screen)
        elif self.mode == 'help':
            self.drawHelp(screen)
        elif self.mode == 'select':
            self.drawSelect(screen)
        elif self.mode == 'options':
            self.drawOptions(screen)

    def drawStart(self, screen):
        self.startScreen.draw(screen)
        self.spawnedNotes.draw(screen)
        self.startButtons.draw(screen)
        self.startHero.draw(screen)

    def drawHelp(self, screen):
        self.helpscreen.draw(screen)
        if self.helpIndex == 0:
            self.nextButton.draw(screen)
        elif self.helpIndex == 1:
            self.backButton.draw(screen)

    def drawSelect(self, screen):
        self.selectScreen.draw(screen)
        self.songFiles.draw(screen)
        file = self.FileFont.render(self.inputText, True, BLACK, None)
        screen.blit(file, (STEP * 3, 285))
        self.backarrow.draw(screen)

    def drawOptions(self, screen):
        self.optionsScreen.draw(screen)
        self.InputModes.draw(screen)
        self.NotesModes.draw(screen)
        self.backarrow.draw(screen)

    def drawGame(self, screen):
        for line in self.Lines:
            line.draw(screen)
        self.Clefs.draw(screen)
        for note in self.Bass:
            if note.x < WIDTH - STEP * 4:
                note.draw(screen)
        for note in self.Treble:
            if note.x < WIDTH - STEP * 4:
                note.draw(screen)
        if not self.pianoOn:
            self.Hero.draw(screen)
            self.heroSpawn.draw(screen)
        if self.hasCPU:
            self.CPU.draw(screen)
        if self.pianoOn:
            self.Portal.draw(screen)
        self.drawNextText(screen)
        self.drawTimeSignature(screen)
        self.drawTempo(screen)

        if self.gameOver or self.isPaused:
            self.drawGameOver(screen)

    def drawGameOver(self, screen):
        msg = 'Song Accuracy * %.2f' % (min(100, self.player.accuracy)) + '%'
        self.gameOverMenu.draw(screen)
        self.gameOverButtons.draw(screen)
        stats = self.GameOverFont.render(msg, True, BLACK)
        screen.blit(stats, (445, 250))

    def generateSongFiles(self):
        x = 200
        songFiles = []
        for i in range(len(GameObjects.SongFile.songs)):
            song = GameObjects.SongFile(x, SFY, i)
            songFiles.append(song)
            x += SFDX
        return songFiles

    def generateInputModes(self):
        y = 155
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

    def getPortal(self):
        result = None
        for portal in self.Portal:
            result = portal
        return result

    def onClick(self, x, y):
        if self.mode == 'select':
            self.clickSelect(x, y)
            buttonPress()
        elif self.mode == 'help':
            self.clickHelp(x, y)
            buttonPress()
        elif self.mode == 'options':
            self.clickModes(x, y)
            buttonPress()
        elif self.mode == 'start':
            self.clickStart(x, y)
            buttonPress()
        elif self.mode == 'play' and self.gameOver or self.isPaused:
            self.clickPlay(x, y)
            buttonPress()

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
        for arrow in self.backarrow:
            if self.pointCollision(arrow, x, y):
                key = arrow.click(arrow.name)
                self.selectMode(key)

    def clickSelect(self, x, y):
        for songFile in self.songFiles:
            if self.pointCollision(songFile, x, y):
                songFile.click()
                self.filename = songFile.id
        for arrow in self.backarrow:
            if self.pointCollision(arrow, x, y):
                key = arrow.click(arrow.name)
                self.selectMode(key)

    def clickStart(self, x, y):
        for button in self.startButtons:
            if self.pointCollision(button, x, y):
                mode = button.name
                self.selectMode(mode)

    def clickHelp(self, x, y):
        next = self.nextButton.sprites()[0]
        back = self.backButton.sprites()[0]
        if self.pointCollision(next, x, y):
            self.helpIndex += 1
            self.updateHelpScreen()
        if self.pointCollision(back, x, y):
            self.helpIndex -= 1
            self.updateHelpScreen()
        for arrow in self.backarrow:
            if self.pointCollision(arrow, x, y):
                key = arrow.click(arrow.name)
                self.selectMode(key)

    def clickPlay(self, x, y):
        for button in self.gameOverButtons:
            if self.pointCollision(button, x, y):
                mode = button.click(button.name)
                self.selectMode(mode)

    def updateHelpScreen(self):
        newImage = self.pageList[self.helpIndex]
        data = self.helpscreen.sprites()[0]
        data.image = GameObjects.load_images(newImage)

    def pointCollision(self, obj, x, y):
        x1, y1, w, h = obj.x, obj.y, obj.width, obj.height
        xPos = set(range(x1 - w, x1 + w))
        yPos = set(range(y1 - h, y1 + h))
        if x in xPos and y in yPos:
            return True
        return False

    def checkFilePath(self, path):
        status = not os.path.isdir(path) and os.path.isfile(path) \
                 and '.mid' in path
        return status

    def drawSurface(self, songFile):
        x, y, w, h = songFile.getRect()
        position = x, y
        size = w, h
        rect = pygame.Rect(position, size)
        image = pygame.Surface(size)
        pygame.draw.rect(image, GREEN, rect)

    def drawNextText(self, screen):
        note = self.NoteFont.render(str(self.currNote), True, BLACK)
        screen.blit(note, (WIDTH // 3 + STEP * 2, HEIGHT // 2 - STEP * 3))
        octave = self.GameFont.render(str(self.currOctave), True, BLACK)
        screen.blit(octave, (WIDTH // 3 + STEP * 6, HEIGHT // 2 + STEP))
        acc = "Accuracy: %.2f" % (min(100, self.player.accuracy)) + '%'
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
        screen.blit(result, (3 * STEP, NOTESTEP))

    def clefCollision(self):
        try:
            for musicNote in self.Bass:
                if pygame.sprite.spritecollide(musicNote, self.Clefs, False):
                    note = musicNote.Note
                    musicNote.kill()
                    self.player.notesList.remove(note)
                    break
            for musicNote in self.Treble:
                if pygame.sprite.spritecollide(musicNote, self.Clefs, False):
                    note = musicNote.Note
                    musicNote.kill()
                    self.player.notesList.remove(note)
                    break
        except:
            pass

    def noteCollision(self):
        if not self.pianoOn:
            try:
                self.heroCollision()
            except:
                pass
        else:
            self.pianoCollision()
            self.cpuCollision()

    def pianoCollision(self):
        portal = self.getPortal()
        if not self.pianoTargets == None:
            for musicNote in self.pianoTargets:
                if self.inputNote() and pygame.sprite.collide_rect(portal, musicNote):
                    musicNote.kill()
                    self.player.hitNote(musicNote)
                    self.player.notesList.remove(musicNote.Note)
                    portal.hit(1)
                else:
                    portal.hit(2)
            self.player.accuracy = ((self.player.score / self.total * 100))

    def heroCollision(self):
        for musicNote in self.targetNotes:
            if pygame.sprite.collide_circle(musicNote, self.getHero()):
                if len(self.targetList) == 1:
                    note = musicNote.Note
                    musicNote.Note.playNote()
                    musicNote.kill()
                    self.player.hitNote(musicNote)
                    self.player.notesList.remove(note)
                else:
                    self.hitChord(musicNote, self.targetList)
                self.getNextTarget()
                self.player.accuracy = ((self.player.score / self.total * 100))

        if self.hasCPU:
            self.cpuCollision()

    def cpuCollision(self):
        for note in self.CPUTargets:
            if pygame.sprite.spritecollide(note, self.CPU, False):
                if len(self.targetList) == 1:
                    note.Note.playNote()
                    self.cpuHit(note)
                    self.player.notesList.remove(note.Note)
                    note.kill()
                else:
                    self.hitChord(note, self.CPUList)
        self.moveCPU()

    def moveCPU(self):
        try:
            if not self.hasDual:
                target = self.CPUList[0]
                self.CPUList = []
                height = target.Note.getHeight()
                self.getCPU().cpuMove(height)
        except:
            pass

    def cpuHit(self, note):
        for (i, testnote) in enumerate(self.CPUTargets):
            if testnote == note:
                self.CPUTargets.sprites().pop(i)
                self.player.score += 1

    def hitChord(self, testNote, data):
        if testNote in data:
            for musicNote in data:
                note = musicNote.Note
                note.playNote()
                musicNote.kill()
                self.player.hitNote(musicNote)
                self.player.notesList.remove(note)


    def getNextTarget(self):
        if self.pianoOn:
            x1 = self.getPortal().x
        else:
            x1 = self.getHero().x
        smallestDisplacement = -2 * WIDTH
        targetList = []
        targets = self.targetNotes
        if not targets: return None
        for note in targets:
            x2 = note.x
            disp = self.getDisplacement(x1, x2)
            if disp is None or disp >= smallestDisplacement and disp < 0:
                smallestDisplacement = disp
                targetList.append(note)
        if not targetList == []:
            self.splitNote(targetList)
        self.targetList = targetList
        self.pianoTargets = targetList

    def getNextCPU(self):
        x1 = self.getCPU().x
        smallestDisplacement = -2 * WIDTH
        targetList = []
        targets = self.CPUTargets
        if not targets: return None
        for note in targets:
            x2 = note.x
            disp = self.getDisplacement(x1, x2)
            if disp is None or disp >= smallestDisplacement and disp < 0:
                smallestDisplacement = disp
                targetList.append(note)
        self.CPUList = targetList

    def getDisplacement(self, x1, x2):
        return x1 - x2

    def checkGameStatus(self):
        # checks conditions for game over
        if self.player.notesList == []:
            self.gameOver = True

    def checkLostNotes(self):
        for musicNote in self.Bass:
            if musicNote.x < 0:
                musicNote.kill()
                self.player.notesList.remove(musicNote.Note)
        for musicNote in self.Treble:
            if musicNote.x < 0:
                musicNote.kill()
                self.player.notesList.remove(musicNote.Note)

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
        flags = DOUBLEBUF | HWSURFACE
        screen = pygame.display.set_mode((self.width, self.height), flags)
        # screen.set_alpha(None)
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        self.screen = screen
        try:
            self.inp = pygame.midi.Input(1)
        except:
            self.inp = None
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            if not self.inp == None and self.inp.poll() and self.pianoOn:
                data = self.inp.read(1000)
                self.keyToNote(data)

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
