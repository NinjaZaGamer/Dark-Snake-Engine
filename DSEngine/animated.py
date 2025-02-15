import pygame
from DSEngine.etypes import *
from pygame.locals import *

class Spritesheet:
    def __init__(self, delay: int = 0, *spritesheet):
        self.sheet = []
        self.delay = 0
        for i in spritesheet:
            if type(i) == Image2D:
                #print(i.name)
                self.sheet.append(i)

class AnimationSheet:
    def __init__(self, default: Image2D, **spritesheets):
        self.sheets = spritesheets
        self.default = default

class AnimatedSprite2D(Type2D):
    def __init__(self, sheet: AnimationSheet, layer=1, position=pygame.Vector2(0.0, 0.0)):#, size=pygame.Vector2(0.0, 0.0)):
        self.sprite = pygame.sprite.Sprite()
        self.debug = False
        self.layer = layer
        self.position = position
        self.sprites = sheet
        self.current_sheet = self.sprites.sheets
        self.curent_frame = 0
        self.sheet_length = -1
        self.playing = False
        self.image = self.sprites.default.image
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        super().__init__(layer=self.layer, position=self.position)
    
    def play_sheet(self, name: str):
        self.current_sheet = self.sprites.sheets[name]
        self.frame = 0
        self.sheet_length = len(self.current_sheet.sheet)
        self.playing = True
    
    def render(self, window: Window):
        if self.current_sheet != self.sprites.sheets and self.frame <= self.sheet_length-1:
            self.image = self.current_sheet.sheet[self.frame].image
            self.frame+=1
            self.playing = True
        else:
            self.image = self.sprites.default.image
            self.current_sheet = self.sprites.sheets
            self.frame = 0
            self.sheet_length = -1
            self.playing = False
        window.surface.blit(self.image, self.rect)
        if self.debug:
            pygame.draw.rect(window.surface, (255, 255, 255), self.rect)
        super().render(window)
    
    def move(self, vec: pygame.Vector2):
        self.rect = self.rect.move(vec.x, vec.y)