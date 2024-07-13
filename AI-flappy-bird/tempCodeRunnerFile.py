draw_count = 0
bg_y = 0
draw_cycle = 0
def draw_window(win, bird, pipes, ground):
    global draw_count, bg_y, draw_cycle

    draw_count += 1
    if draw_count == 60:
        draw_count = 0
        draw_cycle += 1
    if draw_cycle <= 2:
        bg_y -=30
    elif draw_cycle <= 5:
        bg_y +=30
        draw_cycle = 0

    win.blit(BG_IMG, (0,bg_y))

    for pipe in pipes:
        pipe.draw(win)
    
    
    ground.move()
    ground.draw(win)

    #bird.move()
    bird.draw(win)
    
    pg.display.update()
