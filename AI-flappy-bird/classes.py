import pygame as pg
import os

BIRD_IMG1 = pg.image.load(os.path.join("AI-flappy-bird","assets","bird1.png"))
BIRD_IMG2 = pg.image.load(os.path.join("AI-flappy-bird","assets","bird2.png"))
BIRD_IMG3 = pg.image.load(os.path.join("AI-flappy-bird","assets","bird3.png"))

BIRD_IMGS = [BIRD_IMG1, BIRD_IMG2, BIRD_IMG3]
for i in range(len(BIRD_IMGS)):
    BIRD_IMGS[i] = pg.transform.scale2x(BIRD_IMGS[i] )


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
        self.count = 0
        self.cycle = 0
        self.img = self.IMGS[0]
        self.height = self.y
    def jump(self):
        self.velo = -10.5
        self.tick_count = 0
        self.height = self.y
    def move(self):
        self.tick_count +=1
        # d is the amount moved by "gravity"
        d = self.velo*self.tick_count + 1.5*self.tick_count**2 
        if d >= 16:
            d = 16
        elif d < 0: # makes movement feel just a bit better
            d -=2

        self.y +=d

        #Only start tilting bird when it's below orginal pos
        if d < 0 or self.y < self.height + 50:
            if self.tilt > self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VELO
    
    def draw(self, win):
        self.count += 1

        if self.count == self.ANIMATION_RATE:
            self.cycle +=1
            self.count = 0
            if self.cycle == 3:
                self.cycle = 0 
            self.img = self.IMGS[self.cycle]

        if self.tilt <= -75:
            self.img = self.IMGS[1]
            self.count = 0
            self.cycle = 1

        rotated_image = pg.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)


    def get_mask(self):
        return pg.mask.from_surface(self.img)
