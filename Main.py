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
import GameObjects
from Settings import *
import pygame


class Game(object):

    def init(self):
        clefs = (GameObjects.TrebleClef(90,186), GameObjects.BassClef(90,504))
        self.Lines = pygame.sprite.Group(GameObjects.Lines.generateStaff())
        self.Clefs = pygame.sprite.Group(clefs)
        self.Hero = pygame.sprite.Group(GameObjects.Hero(WIDTH//2, 135))
        self.Notes = pygame.sprite.Group(GameObjects.MusicNote(WIDTH-90,270))
        self.NextNote = pygame.sprite.Group(GameObjects.NextNote())
        self.NoteFont = pygame.font.SysFont('agency fb', 100)
        self.GameFont = pygame.font.SysFont('agency fb', 30)


    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        hero = self.getHero()
        if keyCode == pygame.K_UP:
           hero.changeDirection(-1)
           hero.move(WIDTH,HEIGHT)
        if keyCode == pygame.K_DOWN:
            hero.changeDirection(1)
            hero.move(WIDTH,HEIGHT)

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        self.Notes.update(WIDTH,HEIGHT)
        self.clefCollision()


    def redrawAll(self, screen):
        for line in self.Lines:
            line.draw(screen)
        self.Clefs.draw(screen)
        for note in self.Notes:
            note.draw(screen)
        self.Hero.draw(screen)
        self.NextNote.draw(screen)
        self.drawNextText(screen)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def getHero(self):
        result = None
        for hero in self.Hero:
            result = hero
        return result

    def drawNextText(self,screen):
        note = self.NoteFont.render("C#", False, BLACK, None)
        screen.blit(note, (WIDTH//2, HEIGHT//2-45))
        octave = self.GameFont.render("4", False, BLACK, None)
        screen.blit(octave, (WIDTH // 2 + STEP*4, HEIGHT // 2+STEP))
        accuracy = self.GameFont.render("Accuracy: 85%", True, BLACK, None)
        screen.blit(accuracy, (WIDTH - 6*STEP, NOTESTEP*2))

    def clefCollision(self):
        for clef in self.Clefs:
            if pygame.sprite.spritecollide(clef, self.Notes, True):
                print('Bye Bye!')

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