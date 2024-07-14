import pygame as pg
import os
import time
from classes import Bird, Pipe, Ground
import neat

config_path = os.path.join("NEAT-config.txt")

def neat_setup(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                         config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(show_species_detail=True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,25)
    print("======================================")
    print(f"Best genome is: {winner}")
    print("======================================")






WHITE = (0,0,0)
BLACK = (255,255,255)
Gen = -1

pg.font.init()
FONT = pg.font.SysFont("comicsans", 45)

WIN_WIDTH = 600
WIN_HEIGHT = 900

BG_IMG = pg.image.load(os.path.join("assets","night.png"))


WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Flappy Bird")


def draw_outline_text(win, FONT, text,x,y):
    inner = FONT.render(text, 1, BLACK)
    outer = FONT.render(text, 1, WHITE)
    win.blit(outer, (x-2,y-2))
    win.blit(outer, (x-2,y+2))
    win.blit(outer, (x+2,y-2))
    win.blit(outer, (x+2,y+2))
    win.blit(inner, (x,y))

draw_count = 0
bg_y = 0
draw_cycle = 0
bg_breath = 3
def draw_score_gen(win, score):
    global Gen
    
    inner_score = FONT.render(f"Score: {score}", 1, BLACK)
    x = WIN_WIDTH - 10 - inner_score.get_width()
    draw_outline_text(win, FONT, f"Score: {score}", x, 10)

    inner_gen = FONT.render(f"Gen: {Gen}", 1, BLACK)
    draw_outline_text(win, FONT, f"Gen: {Gen}", 10, 10)
    

def draw_window(win, birds, pipes, ground, score):
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

    for bird in birds:
        bird.draw(win)

    draw_score_gen(win, score)
    
    pg.display.update()


def main(genomes, config):
    global Gen
    Gen += 1
    birds = []
    nets = []
    ge = []

    for _ , g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(200,200))
        g.fitness = 0
        ge.append(g)



    
    


    clock = pg.time.Clock()
    ground = Ground(790)
    pipes = [Pipe(700)]

    score = 0
    running = True

    while running:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].TOP_PIPE.get_width():
                    pipe_index = 1
        else:
            running = False
            print("!!! No birds left, moving to new gen !!!")
            break   
            
        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.05

            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_index].top_height), abs(bird.y - pipes[pipe_index].bottom)))
            if output[0] > 0.5:
                bird.jump()


        add_pipe = False
        remove = []
        for pipe in pipes:
            pipe.move()

            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 3
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                    print("Bird died to pipe!")
                    
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
                

            if pipe.x + pipe.BOTTOM_PIPE.get_width() < 0:
                remove.append(pipe)

        if add_pipe:
            score +=1
            for g in ge:
                g.fitness += 5

            pipes.append(Pipe(620))
            add_pipe = False

        for pipe in remove:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 790:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)
                print("bird died to ground QQ")
            elif bird.y <0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)
                print("bird flew too high QQ")

        draw_window(WIN, birds, pipes, ground, score)



if __name__ == "__main__":
    neat_setup(config_path)




