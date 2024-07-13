import pygame as pg
import os
import time
from classes import Bird

WIN_WIDTH = 600
WIN_HEIGHT = 900



PIPE_IMG3 = pg.transform.scale2x(pg.image.load(os.path.join("AI-flappy-bird","assets","pipe.png")))
GND_IMG = pg.transform.scale2x(pg.image.load(os.path.join("AI-flappy-bird","assets","ground.png")))
BG_IMG = pg.image.load(os.path.join("AI-flappy-bird","assets","night.png"))


WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Flappy Bird")




def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.move()
    bird.draw(win)
    
    pg.display.update()


def main():
    clock = pg.time.Clock()
    birdy = Bird(200,200)


    running = True

    while running:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        
        draw_window(WIN, birdy)

    pg.quit()

if __name__ == "__main__":
    main()




