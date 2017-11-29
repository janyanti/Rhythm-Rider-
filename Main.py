##############################################
# Main | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################
import os
import string
import MusicAnalyzer
import time
import GameObjects
from Player import Player
from Settings import *
import pygame
import queue
import threading

q = queue.Queue()


class Game(object):
    def init(self):
        self.modes = MODES
        self.mode = 'start'
        self.player = Player(MusicAnalyzer.song)
        self.timer = 0
        self.NextNote = pygame.sprite.Group(GameObjects.NextNote())
        self.NoteFont = pygame.font.SysFont('alba', 100)
        self.GameFont = pygame.font.SysFont('alba', 35)
        self.timeFont = pygame.font.Font('assets/Aruvarb.ttf', 116)
        self.inputText = ''
        self.gameMode = 'bass'
        self.hasCPU = True

        # start screen
        self.initStart()
        self.initSelect()


        # help screen
        # helpSprite = pygame.sprite.Sprite()
        # helpSprite.image = pygame.image.load('assets/helpscreen.png')
        # helpSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        # self.helpscreen = pygame.sprite.Group(helpSprite)

    def mousePressed(self, x, y):
        if self.mode == 'start':
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
        playButton = GameObjects.Button(640, 540, 'select')
        helpButton = GameObjects.Button(640, 650, 'help')
        self.startButtons = pygame.sprite.Group(playButton, helpButton)

    def initSelect(self):
        # define screen/attributes for this mode
        selectSprite = pygame.sprite.Sprite()
        selectSprite.image = pygame.image.load('assets/selectscreen.png')
        selectSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.selectScreen = pygame.sprite.Group(selectSprite)

    def selectMode(self, mode):
        command = self.modes[mode]
        eval(command)
        self.mode = mode

    def initGame(self):
        clefs = (GameObjects.TrebleClef(90, 186), GameObjects.BassClef(90, 504))
        self.Lines = pygame.sprite.Group(GameObjects.Lines.generateStaff())
        self.Clefs = pygame.sprite.Group(clefs)
        self.Notes = pygame.sprite.Group(self.player.musicNotes)
        self.Hero = pygame.sprite.Group(GameObjects.Hero(WIDTH // 2, 135))
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
        self.splitNote(self.targetNotes[0])
        # print(self.targetNotes)
        self.numerator, self.denominator = self.player.song.getTimeSignature()

    def selectInput(self, char):
        self.inputText += char

    def splitNote(self, note):
        name = note.getNoteName()
        octave = note.getOctave()
        self.currNote = name
        self.currOctave = octave

    def keyPressed(self, keyCode, modifier):
        if self.mode == 'play':
            hero = self.getHero()
            if keyCode == pygame.K_UP:
                hero.changeDirection(-1)
                hero.move(WIDTH, HEIGHT)
            if keyCode == pygame.K_DOWN:
                hero.changeDirection(1)
                hero.move(WIDTH, HEIGHT)
        if self.mode == 'select':
            if keyCode == pygame.K_BACKSPACE:
                self.inputText = self.inputText[:-1]
            elif not keyCode == pygame.K_RETURN:
                char = chr(keyCode)
                if char in string.printable:
                    self.selectInput(char)
            else:
                time.sleep(0.5)
                self.selectMode('play')

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        self.timer += 1
        if self.mode == 'start':
            self.startHero.update()
        if self.timer % 5 == 0:
            spawn = self.getStartHero().spawnNote()
            self.spawnedNotes.add(spawn)
        self.spawnedNotes.update()
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


    def drawStart(self, screen):
        self.startScreen.draw(screen)
        self.spawnedNotes.draw(screen)
        self.startButtons.draw(screen)
        self.startHero.draw(screen)

    def drawSelect(self, screen):
        self.selectScreen.draw(screen)
        file = self.GameFont.render(self.inputText, True, BLACK, None)
        screen.blit(file, (STEP * 3, 285))

    def drawGame(self, screen):
        for line in self.Lines:
            line.draw(screen)
        self.Clefs.draw(screen)
        for note in self.Notes:
            note.draw(screen)
        self.Hero.draw(screen)
        if self.hasCPU:
            self.CPU.draw(screen)
        self.NextNote.draw(screen)
        self.drawNextText(screen)
        self.drawTimeSignature(screen)


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
        for button in self.startButtons:
            test = button.rect
            if test.collidepoint(x, y):
                mode = button.name
                self.selectMode(mode)

    def drawNextText(self, screen):
        note = self.NoteFont.render(str(self.currNote), True, BLACK, None)
        screen.blit(note, (WIDTH // 2, HEIGHT // 2 - 45))
        octave = self.GameFont.render(str(self.currOctave), True, BLACK, None)
        screen.blit(octave, (WIDTH // 2 + STEP * 4, HEIGHT // 2 + STEP))
        acc = "Accuracy: %.2f" % (self.player.accuracy) + '%'
        accuracy = self.GameFont.render(acc, True, BLACK, None)
        screen.blit(accuracy, (WIDTH - 10 * STEP, NOTESTEP * 2))

    def drawTimeSignature(self, screen):
        numer = self.timeFont.render(str(self.numerator), True, BLACK, None)
        denom = self.timeFont.render(str(self.denominator), True, BLACK, None)
        screen.blit(numer, (STEP * 6, -NOTESTEP * 5))
        screen.blit(denom, (STEP * 6, -NOTESTEP))
        screen.blit(numer, (STEP * 6, NOTESTEP * 17))
        screen.blit(denom, (STEP * 6, NOTESTEP * 21))

    def worker(self):
        print('working')
        self.count += 1
        q.put(self.count)
        time.sleep(1)

    def clefCollision(self):
        for clef in self.Clefs:
            if pygame.sprite.spritecollide(clef, self.Notes, True):
                self.player.missedNotes += 1
                self.targetNotes.pop(0)
                # self.splitNote(self.player.notesList[0])

    def noteCollision(self):
        for note in self.Notes:
            if pygame.sprite.spritecollide(note, self.Hero, False):
                note.Note.playNote()
                note.kill()
                self.player.hitNote(note)
                self.splitNote(self.targetNotes[0])
                self.player.accuracy = ((self.player.score / self.total * 100))
        if self.hasCPU:
            self.cpuCollision()

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

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        self.screen = screen
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
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
