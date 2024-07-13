import pygame as pg
import os
import time
from classes import Bird, Pipe, Ground

WIN_WIDTH = 600
WIN_HEIGHT = 900

BG_IMG = pg.image.load(os.path.join("assets","night.png"))


WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Flappy Bird")



draw_count = 0
bg_y = 0
draw_cycle = 0
bg_breath = 3
def draw_window(win, bird, pipes, ground):
    global draw_count, bg_y, draw_cycle, bg_breath

    draw_count += 1
    if draw_count == 30:
        draw_count = 0
        draw_cycle += 1
        if draw_cycle == 5:
            draw_cycle = 1

        if draw_cycle <= 2:
            bg_y -=bg_breath
        else:
            bg_y +=bg_breath


    win.blit(BG_IMG, (0,bg_y))

    for pipe in pipes:
        pipe.draw(win)
    
    
    ground.move()
    ground.draw(win)
    bird.draw(win)
    
    pg.display.update()


def main():
    score = 0
    add_pipe = False


    clock = pg.time.Clock()
    birdy = Bird(230,400)
    ground = Ground(790)
    pipes = [Pipe(700)]


    running = True

    while running:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        remove = []
        for pipe in pipes:
            if pipe.collide(birdy):
                print("Collided, game over QQ")

            if pipe.x + pipe.BOTTOM_PIPE.get_width() < 0:
                remove.append(pipe)

            if not pipe.passed and pipe.x < birdy.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()


        if add_pipe:
            score +=1
            print(f"Current score: {score}")
            pipes.append(Pipe(700))
            add_pipe = False

        for pipe in remove:
            pipes.remove(pipe)

        draw_window(WIN, birdy, pipes, ground)

    pg.quit()

if __name__ == "__main__":
    main()




