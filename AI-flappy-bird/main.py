import pygame as pg
import os
import time

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMG1 = pg.image.load(os.path.join("AI-flappy-bird","assets","bird1.png"))
BIRD_IMG2 = pg.image.load(os.path.join("AI-flappy-bird","assets","bird2.png"))
BIRD_IMG3 = pg.image.load(os.path.join("AI-flappy-bird","assets","bird3.png"))

BIRD_IMGS = [BIRD_IMG1, BIRD_IMG2, BIRD_IMG3]
for image in BIRD_IMGS:
    image = pg.transform.scale2x(image)

BIRD_IMG3 = pg.transform.scale2x(pg.image.load(os.path.join("AI-flappy-bird","assets","pipe.png")))
GND_IMG = pg.transform.scale2x(pg.image.load(os.path.join("AI-flappy-bird","assets","ground.png")))
BG_IMG = pg.transform.scale2x(pg.image.load(os.path.join("AI-flappy-bird","assets","night.png")))



class Bird:
    IMGS = BIRD_IMGS
    ANIMATION_RATE = 5
    ROT_VELO = 20
    MAX_ROT = 25

    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velo = 0
        self.img_state = 0
        self.img = self.IMGS[0]
        self.height = self.y
    def jump(self):
        self.velo = -10.5
        self.tick_count = 0
        self.height = self.y
    def move(self):
        self.tick_count +=1


