import pygame as pg
import os
import time
from classes import Bird, Pipe, Ground

pg.font.init()
FONT = pg.font.SysFont("comicsans", 45)

WIN_WIDTH = 600
WIN_HEIGHT = 900

BG_IMG = pg.image.load(os.path.join("assets","night.png"))


WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Flappy Bird")



draw_count = 0
bg_y = 0
draw_cycle = 0
bg_breath = 3
def draw_score(win, score):
    WHITE = (0,0,0)
    BLACK = (255,255,255)
    inner_score = FONT.render(f"Score: {score}", 1, BLACK)
    outer_score = FONT.render(f"Score: {score}", 1, WHITE)
    x = WIN_WIDTH - 10 - inner_score.get_width()
    y = 10
    win.blit(outer_score, (x-2,y-2))
    win.blit(outer_score, (x-2,y+2))
    win.blit(outer_score, (x+2,y-2))
    win.blit(outer_score, (x+2,y+2))
    win.blit(inner_score, (x,y))

def draw_window(win, bird, pipes, ground, score):
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
    draw_score(win, score)
    
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
            pipes.append(Pipe(620))
            add_pipe = False

        for pipe in remove:
            pipes.remove(pipe)

        if birdy.y + birdy.img.get_height() >= 790:
            print("you ded, game over")

        draw_window(WIN, birdy, pipes, ground,score)

    pg.quit()

if __name__ == "__main__":
    main()




