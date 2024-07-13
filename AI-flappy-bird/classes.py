import pygame as pg
import os
import random

def scale_image(image, scale_factor):
    width = image.get_width() * scale_factor
    height = image.get_height() * scale_factor
    return pg.transform.scale(image, (width, height))


BIRD_IMG1 = pg.image.load(os.path.join("assets","bird1.png"))
BIRD_IMG2 = pg.image.load(os.path.join("assets","bird2.png"))
BIRD_IMG3 = pg.image.load(os.path.join("assets","bird3.png"))
BIRD_IMGS = [BIRD_IMG1, BIRD_IMG2, BIRD_IMG3]
for i in range(len(BIRD_IMGS)):
    BIRD_IMGS[i] = scale_image(BIRD_IMGS[i], 2)

PIPE_IMG = scale_image(pg.image.load(os.path.join("assets","pipe.png")),2)
GND_IMG = scale_image(pg.image.load(os.path.join("assets","ground.png")),2)


SCROLL_VELO = 5

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

class Pipe:
    GAP = 220
    VELO = SCROLL_VELO

    def __init__(self, x):
        self.x = x
        self.top_height = 0

        self.top = 0
        self.bottom = 0

        self.TOP_PIPE = pg.transform.flip(PIPE_IMG, flip_x=False, flip_y=True)
        self.BOTTOM_PIPE = PIPE_IMG

        self.passed = False
        self.set_height() 


    def set_height(self):
        self.top_height = random.randint(50,500)
        self.top = self.top_height - self.TOP_PIPE.get_height()
        self.bottom = self.top_height + self.GAP

    def move(self):
        self.x -= self.VELO

    def draw(self,win):
        win.blit(self.TOP_PIPE, (self.x, self.top))
        win.blit(self.BOTTOM_PIPE, (self.x, self.bottom))
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pg.mask.from_surface(self.TOP_PIPE)
        bottom_mask = pg.mask.from_surface(self.BOTTOM_PIPE)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_collide_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_collide_point = bird_mask.overlap(top_mask, top_offset)

        if b_collide_point or t_collide_point:
            return True
        else:
            return False


class Ground:
    VELO = SCROLL_VELO
    WIDTH = GND_IMG.get_width()
    IMG = GND_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELO
        self.x2 -= self.VELO

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))



