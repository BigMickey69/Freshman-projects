import pygame, random
pygame.font.init()
score_font = pygame.font.SysFont('comicsans', 26)


def create_zero_array(n):
    a = [0]*n
    for i in range(n):
        a[i] = [0]*n
    return a

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakey Snakey slither slither")
QQ_img = pygame.image.load("QQ.png")
Running = 1
timer = 0
startingtimer=0
apple_color = (255,100,100)
player_color = (250, 191, 41)
n = 20
score = 0
command = "right"
chance = 0
apple = 0


grid = create_zero_array(20)

grid [0][0] = 1
p_cords = [0,0]
old_p_cords=[[0,0]]

eyes_img = pygame.image.load("eyes.png")


def draw_grid(grid, head_position, direction):
    
    global n
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 2:
                pygame.draw.rect(WIN, apple_color, pygame.Rect((i*n*1.5,j*n*1.5,n*1.5,n*1.5)))
            elif grid[i][j] == 1:
                pygame.draw.rect(WIN, player_color, pygame.Rect((i*n*1.5,j*n*1.5,n*1.5,n*1.5)))
            elif grid[i][j] == 0:
                pygame.draw.rect(WIN, (238,228,218), pygame.Rect((i*n*1.5,j*n*1.5,n*1.5,n*1.5)))
    if direction == "right":
        var_y = -6
        var_x = 5
        rotated_eyes_img = eyes_img
    elif direction == "up":
        var_y = -16
        var_x = -5
        rotated_eyes_img = pygame.transform.rotate(eyes_img, 90)
    elif direction == "down":
        var_y = 6
        var_x = -5
        rotated_eyes_img = pygame.transform.rotate(eyes_img, -90)
    elif direction == "left":
        var_y = -6
        var_x = -16
        rotated_eyes_img = pygame.transform.rotate(eyes_img, 180)

    WIN.blit(rotated_eyes_img, (head_position[0]*n*1.5+var_x, head_position[1]*n*1.5+var_y))
        

def player_movement():
    global grid, p_cords, score, command, chance, apple
    match command:
        case "right":
                if p_cords[0] != n-1:
                    chance = 0
                    old_p_cords.append(p_cords)
                    grid[p_cords[0]][p_cords[1]] = 0
                    if grid[p_cords[0]+1][p_cords[1]] == 2:
                        score +=1
                        apple = 0
                    elif grid[p_cords[0]+1][p_cords[1]] == 1:
                        command = "lost"
                    grid[p_cords[0]+1][p_cords[1]] = 1
                    p_cords = [p_cords[0]+1, p_cords[1]]
                else:
                     if chance == 2:
                        command = "lost"
                     else:
                        chance += 1

        case "left":
            if p_cords[0] != 0:
                chance = 0
                old_p_cords.append(p_cords)
                grid[p_cords[0]][p_cords[1]] = 0
                if grid[p_cords[0]-1][p_cords[1]] == 2:
                        score +=1
                        apple = 0
                elif grid[p_cords[0]-1][p_cords[1]] == 1:
                    command = "lost"
                grid[p_cords[0]-1][p_cords[1]] = 1
                p_cords = [p_cords[0]-1, p_cords[1]]
            else:
                if chance == 2:
                    command = "lost"
                else:
                    chance += 1
        case "up":
            if p_cords[1] != 0:
                old_p_cords.append(p_cords)
                grid[p_cords[0]][p_cords[1]] = 0
                if grid[p_cords[0]][p_cords[1]-1] == 2:
                        score +=1
                        apple = 0
                elif grid[p_cords[0]][p_cords[1]-1] == 2:
                        command = "lost"
                grid[p_cords[0]][p_cords[1]-1] = 1
                p_cords = [p_cords[0], p_cords[1]-1]
            else:
                     if chance == 2:
                        command = "lost"
                     else:
                        chance += 1
        case "down":
            if p_cords[1] != n-1:
                old_p_cords.append(p_cords)
                grid[p_cords[0]][p_cords[1]] = 0
                if grid[p_cords[0]][p_cords[1]+1] == 2:
                        score +=1
                        apple = 0
                if grid[p_cords[0]][p_cords[1]-1] == 2:
                        command = "lost"
                grid[p_cords[0]][p_cords[1]+1] = 1
                p_cords = [p_cords[0], p_cords[1]+1]
            else:
                     if chance == 2:
                        command = "lost"
                     else:
                        chance += 1

def tail():
    global grid, old_p_cords,score
    print(f"current old_p_cords: {old_p_cords}")
    while(len(old_p_cords)>score):
        old_cords = old_p_cords[0]
        grid[old_cords[0]][old_cords[1]] = 0
        old_p_cords.pop(0)
    for i in range(score):
        grid[old_p_cords[i][0]][old_p_cords[i][1]] = 1


def pick_random(grid):
    global n
    temp = []
    for i in range(n):
        for j in range(n):
            if grid[i][j]==0:
                temp.append([i,j])
    returner = random.choice(temp)
    print ("spawning apple at ", returner)
    return returner
def draw_apple():
    global apple
    if apple == 0:
        apple_cords = pick_random(grid)
        grid[apple_cords[0]][apple_cords[1]] = 2
        apple = 1
            

def main():
    global Running, timer,n, p_cords, score, startingtimer, old_p_cords, command
    starttail = 0
    startapple = 0
    direction = "right"
    spawn = True
    clock = pygame.time.Clock()
    tickrate = 14

    while Running:
        clock.tick(tickrate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = 0
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tickrate = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    tickrate = 14

        if command != "lost": # if feels better than elif
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and command != "down":
                command = "up"
                direction = "up"
            if key[pygame.K_s]and command != "up":
                command = "down"
                direction = "down"
            if key[pygame.K_a] and command != "right":
                command = "left"
                direction = "left"
            if key[pygame.K_d] and command != "left":
                command = "right"
                direction = "right"


        startingtimer+=1
        timer += 1
        if startingtimer == 10:
            starttail =1
            startapple = 1
        if timer==160 and spawn:
            apple_cords = pick_random(grid)
            grid[apple_cords[0]][apple_cords[1]] = 2
            timer = 0

        WIN.fill((238,228,218))
        if(startapple):
            draw_apple()
        player_movement()
        if (starttail):
            tail()
        draw_grid(grid, p_cords, direction)
        score_text = score_font.render(f"Score: {score}", 1, (25,1,5))
        text_rect = score_text.get_rect(center=(530, 20))
        WIN.blit(score_text, text_rect)
        if command == "lost":
            print("you lost QQ")
            WIN.blit(QQ_img, (0,0))
            starttail = 0
            startapple = 0
            spawn = False
        

        pygame.display.update()



if __name__ == "__main__":
    main()
    