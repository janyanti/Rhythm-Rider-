##############################################
# Main | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################
import os
import math
import pygame
import time
import GameObjects
from Settings import *
import pygame
import queue
import threading

q = queue.Queue()


class Game(object):
    def init(self):
        self.mode = 'start'
        self.timer = 0
        self.NextNote = pygame.sprite.Group(GameObjects.NextNote())
        self.NoteFont = pygame.font.SysFont('agency fb', 100)
        self.GameFont = pygame.font.SysFont('agency fb', 30)
        self.timeFont = pygame.font.Font('assets/Aruvarb.ttf', 116)

        # start screen
        startSprite = pygame.sprite.Sprite()
        startSprite.image = pygame.image.load('assets/startscreen.png')
        startSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.startScreen = pygame.sprite.Group(startSprite)
        self.startHero = pygame.sprite.Group(GameObjects.startHero())
        self.spawnedNotes = pygame.sprite.Group()

        # help screen
        # helpSprite = pygame.sprite.Sprite()
        # helpSprite.image = pygame.image.load('assets/helpscreen.png')
        # helpSprite.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        # self.helpscreen = pygame.sprite.Group(helpSprite)

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def initGame(self):
        clefs = (GameObjects.TrebleClef(90, 186), GameObjects.BassClef(90, 504))
        self.Lines = pygame.sprite.Group(GameObjects.Lines.generateStaff())
        self.Clefs = pygame.sprite.Group(clefs)
        self.Notes = pygame.sprite.Group(GameObjects.MusicNote(WIDTH * 2, 270))
        self.Notes.add(GameObjects.MusicNote(WIDTH * 2 + 180, 270))
        self.Hero = pygame.sprite.Group(GameObjects.Hero(WIDTH // 2, 135))

    def keyPressed(self, keyCode, modifier):
        if self.mode == 'play':
            hero = self.getHero()
            if keyCode == pygame.K_UP:
                hero.changeDirection(-1)
                hero.move(WIDTH, HEIGHT)
            if keyCode == pygame.K_DOWN:
                hero.changeDirection(1)
                hero.move(WIDTH, HEIGHT)

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
            self.clefCollision()
            self.noteCollision()

    def redrawAll(self, screen):
        if self.mode == 'start':
            self.startScreen.draw(screen)
            self.startHero.draw(screen)
            self.spawnedNotes.draw(screen)
        elif (self.mode == 'play'):
            for line in self.Lines:
                line.draw(screen)
            self.Clefs.draw(screen)
            for note in self.Notes:
                note.draw(screen)
            self.Hero.draw(screen)
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

    def getStartHero(self):
        result = None
        for hero in self.startHero:
            result = hero
        return result

    def drawNextText(self, screen):
        note = self.NoteFont.render("C#", False, BLACK, None)
        screen.blit(note, (WIDTH // 2, HEIGHT // 2 - 45))
        octave = self.GameFont.render("4", False, BLACK, None)
        screen.blit(octave, (WIDTH // 2 + STEP * 4, HEIGHT // 2 + STEP))
        accuracy = self.GameFont.render("Accuracy: 85%", True, BLACK, None)
        screen.blit(accuracy, (WIDTH - 6 * STEP, NOTESTEP * 2))

    def drawTimeSignature(self, screen):
        numer = self.timeFont.render('4', False, BLACK, None)
        denom = self.timeFont.render('4', False, BLACK, None)
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
                print('Bye Bye!')
                print(time.time())

    def noteCollision(self):
        for note in self.Notes:
            if pygame.sprite.spritecollide(note, self.Hero, False):
                note.Note.playNote()
                note.kill()

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
        print('hi')
        # if self.count == 0:
        #     self.t.start()
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
            # try:
            #     print(q.get())
            # except:
            #     print('oh well')
            pygame.display.flip()

        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
