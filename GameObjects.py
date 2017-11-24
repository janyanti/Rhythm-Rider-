##############################################
# Game Objects | 15-112 Term Project
#  Joel Anyanti | Janyanti
##############################################

##############################################
# Imports
##############################################

import pygame
import os
import Note
from Settings import *

refNote = Note.Notes(58, 112, 144, 0)

class GameObject(pygame.sprite.Sprite):
    # Generic game sprite object
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()
        self.velocity = (0, 0)
        self.angle = 0

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()
        # wrap around, and update the rectangle again
        if self.rect.left > screenWidth:
            self.x -= screenWidth + self.width
        elif self.rect.right < 0:
            self.x += screenWidth + self.width
        if self.rect.top > screenHeight:
            self.y -= screenHeight + self.height
        elif self.rect.bottom < 0:
            self.y += screenHeight + self.height
        self.updateRect()


class Hero(GameObject):
    img = pygame.image.load('assets/hero.png')
    direction = 1

    def __init__(self, x, y, ):
        super().__init__(x, y, Hero.img, 20)
        self.dy = Lines.margin
        self.dx = 0
        # self.velocity = (self.dx, self.dy*Hero.direction)

    def changeDirection(self, dir):
        if dir == Hero.direction:
            return
        Hero.direction = dir

    def move(self, screenWidth, screenHeight):
        self.y += self.dy * Hero.direction
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.updateRect()
        # wrap around, and update the rectangle again
        if self.rect.left > screenWidth:
            self.x -= screenWidth + self.width
        elif self.rect.right < 0:
            self.x += screenWidth + self.width
        if self.rect.top > screenHeight:
            self.y -= screenHeight + self.height
        elif self.rect.bottom < 0:
            self.y += screenHeight + self.height
        self.updateRect()


class MusicNote(GameObject):
    image = pygame.image.load('assets/notehead.png')
    stem = pygame.image.load('assets/stem.png')
    sharp = pygame.image.load('assets/sharp.png')

    def __init__(self, x, y=0, img=0, rad=20):
        super(MusicNote, self).__init__ \
            (x, y, MusicNote.image, rad)
        self.Note = Note.Notes.toNote([144, 60, 112, 0])
        self.velocity = (-5, 0)
        self.y = self.Note.getHeight()

    def draw(self, screen):
        print(self.y)
        self.rect = self.getRect()
        screen.blit(self.image, self.rect)
        stemRect = self.noteType()
        screen.blit(MusicNote.stem, stemRect)
        sharpRect = self.getSharpRect()
        if self.Note.isAccidental():
            screen.blit(MusicNote.sharp, sharpRect)

    def getRect(self):
        # gets Rect attribute of note
        w, h = self.image.get_size()
        self.width, self.height = w, h
        rect = pygame.Rect(self.x - w // 2, self.y - h // 2, w, h)
        return rect

    def getSharpRect(self):
        # gets position of accidental
        x, y = self.x - 40, self.y + 5
        w, h = 26, 60
        rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
        return rect

    def noteType(self):
        # returns the orientation of a given note
        x, y = self.x, self.y
        upNote = pygame.Rect(x + 15, y-105, x+17, y)
        downNote = pygame.Rect(x - 19, y, x-21, y+105)
        clef = self.Note.getClef()
        noteID = self.Note.noteID
        if clef is "Treble":
            if noteID >= 71:
                return downNote
            return upNote
        if clef is 'Bass':
            if noteID >= 50:
                return downNote
            return upNote

    def update(self, screenWidth, screenHeight):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()


class Lines(pygame.sprite.Sprite):
    lineSpace = HEIGHT / 16
    margin = STEP
    clefLines = 5

    def __init__(self, x, y):
        super(Lines, self).__init__()
        self.x = x
        self.y = y
        self.height = 2
        self.width = WIDTH - 2 * Lines.margin
        w, h = self.width, self.height
        self.rect = pygame.Rect(self.x, self.y, w, h)

    def draw(self, screen):
        rect = self.rect
        pygame.draw.rect(screen, BLACK, rect, 0)

    @staticmethod
    def generateStaff():
        # makes music sheet ledger for game
        linesList = []
        x = Lines.margin
        y = Lines.margin * 4

        # Treble Clef Lines
        for i in range(Lines.clefLines):
            line = Lines(x, y)
            linesList.append(line)
            y += Lines.margin

        y += Lines.margin * 6
        # Bass Clef Lines
        for i in range(Lines.clefLines):
            line = Lines(x, y)
            linesList.append(line)
            y += Lines.margin

        linesList.append(LedgerLine(STEP,STEP*4))
        linesList.append(LedgerLine(WIDTH-STEP, STEP * 4))
        return linesList

class LedgerLine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(LedgerLine, self).__init__()
        self.x = x
        self.y = y
        self.height = 450
        self.width = 4
        w, h = self.width, self.height
        self.rect = pygame.Rect(self.x, self.y, w, h)

    def draw(self, screen):
        rect = self.rect
        pygame.draw.rect(screen, BLACK, rect, 0)


class TrebleClef(GameObject):
    image = pygame.image.load('assets/treble.png')

    def __init__(self, x, y):
        super(TrebleClef, self).__init__(x, y, TrebleClef.image, 20)


class BassClef(GameObject):
    image = pygame.image.load('assets/bass.png')

    def __init__(self, x, y):
        super(BassClef, self).__init__(x, y, BassClef.image, 20)


class NextNote(pygame.sprite.Sprite):
    # should be a part of player class
    def __init__(self):
        super(NextNote, self).__init__()
        self.x = WIDTH // 2
        self.y = HEIGHT // 2 + NOTESTEP
        self.width = NOTESTEP * 12
        self.height = NOTESTEP * 6
        self.defineRect()

    def defineRect(self):
        w, h = self.width, self.height
        x, y = self.x, self.y
        self.rect = pygame.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
        self.image = pygame.Surface((w, h))
        self.image.fill(WHITE)
