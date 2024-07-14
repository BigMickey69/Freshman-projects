import pygame, random
pygame.font.init()

num_font = pygame.font.SysFont('comicsans', 50)
num_font2 = pygame.font.SysFont('comicsans', 48)
num_font3 = pygame.font.SysFont('comicsans', 43)
num_font4 = pygame.font.SysFont('comicsans', 42,'bold')
num_font5 = pygame.font.SysFont('Arial Black', 95)
score_font = pygame.font.SysFont('comicsans', 44)
highscore_font = pygame.font.SysFont('comicsans', 16)
WIDTH, HEIGHT = 650, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 as basic as can BE!")

splash = pygame.image.load("splash.png")
background = pygame.image.load("grid.png").convert_alpha()
win_text = pygame.image.load("win.png")
overlay = pygame.image.load("overlay.png")
button_img = pygame.image.load("button.png")
bg_X, bg_Y = 75, 300

grid = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

A,B,C,D = 15,15+106+15,15+106+15+106+15,15+106+15+106+15+106+15
next_bloc = []
frame = 0
dog = 0
pog = 0
spawn_state = False
won = False
score = 0
running = True





class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

restart = Button(600,200,button_img,1)

def reset_grid():
    global grid
    grid = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def num_to_color(num):
    if num == 2: return (238,228,218)
    elif num == 4: return (238,225,201)
    elif num == 8: return (243,178,122)
    elif num == 16: return (246,150,100)
    elif num == 32: return (247,124,95)
    elif num == 64: return (247,95,59)
    elif num == 128: return (238,208,115)
    elif num == 256: return (237,204,97)
    elif num == 512: return (234,194,70)
    elif num == 1024: return (234,184,20)
    elif num == 2048: return (234,164,0)

def pick_random(grid):
    temp=[]
    cat= [2,2,4]
    for i in range(16):
        if grid[i] == 0:
            temp.append(i)
    dog = [random.choice(temp), random.choice(cat)]
    return dog
def num_to_grid(num):
    if num == 1: return [A,A]
    elif num == 2: return [B,A]
    elif num == 3: return [C,A]
    elif num == 4: return [D,A]
    elif num == 5: return [A,B]
    elif num == 6: return [B,B]
    elif num == 7: return [C,B]
    elif num == 8: return [D,B]
    elif num == 9: return [A,C]
    elif num == 10: return [B,C]
    elif num == 11: return [C,C]
    elif num == 12: return [D,C]
    elif num == 13: return [A,D]
    elif num == 14: return [B,D]
    elif num == 15: return [C,D]
    elif num == 16: return [D,D]

def draw_2bloc(SQR):
    bloc = num_font.render("2", 1, (119,110,101))
    pygame.draw.rect(WIN, (238,228,218), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+38,SQR[1]+16))
def draw_4bloc(SQR):
    bloc = num_font.render("4", 1, (119,110,101))
    pygame.draw.rect(WIN, (238,225,201), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+38,SQR[1]+16))
def draw_8bloc(SQR):
    bloc = num_font.render("8", 1, (249,246,242))
    pygame.draw.rect(WIN, (243,178,122), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+38,SQR[1]+16))
def draw_16bloc(SQR):
    bloc = num_font.render("16", 1, (249,246,242))
    pygame.draw.rect(WIN, (246,150,100), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+28,SQR[1]+16))
def draw_32bloc(SQR):
    bloc = num_font.render("32", 1, (249,246,242))
    pygame.draw.rect(WIN, (247,124,95), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+24,SQR[1]+16))
def draw_64bloc(SQR):
    bloc = num_font.render("64", 1, (249,246,242))
    pygame.draw.rect(WIN, (247,95,59), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+24,SQR[1]+16))
def draw_128bloc(SQR):
    bloc = num_font.render("128", 1, (249,246,242))
    pygame.draw.rect(WIN, (238,208,115), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+13,SQR[1]+16))
def draw_256bloc(SQR):
    bloc = num_font2.render("256", 1, (249,246,242))
    pygame.draw.rect(WIN, (237,204,97), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+12,SQR[1]+19))
def draw_512bloc(SQR):
    bloc = num_font2.render("512", 1, (249,246,242))
    pygame.draw.rect(WIN, (234,194,70), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+13,SQR[1]+19))
def draw_1024bloc(SQR):
    bloc = num_font3.render("1024", 1, (249,246,242))
    pygame.draw.rect(WIN, (234,184,20), SQR,0,3)
    WIN.blit(bloc, (SQR[0]+5,SQR[1]+22))
def draw_2048bloc(SQR):
    bloc = num_font4.render("2048", 1, (249,246,242))
    pygame.draw.rect(WIN, (234,164,0), SQR,0,3)
    WIN.blit(bloc, (SQR[0],SQR[1]+22))

def down_up_calc(grid):
    global score
    for j in range(4):
            stack = [grid[0+j], grid[4+j], grid[8+j], grid[12+j]]
            for i in range(4):
                if stack[i] == 0:
                    stack.pop(i)
                    stack.insert(0,0)
            for i in range(3,-1,-1):
                if stack [i] == stack[i-1]:
                    stack [i] = stack[i]*2
                    score = score + stack[i]
                    stack[i-1] = 0
            for i in range(4):
                if stack [i] == 0:
                    stack.pop(i)
                    stack.insert(0, 0)
            grid[0+j], grid[4+j], grid[8+j], grid[12+j] = stack[0], stack[1], stack[2], stack[3]
def up_down_calc(grid):
    global score
    for j in range(4):
            stack = [grid[0+j], grid[4+j], grid[8+j], grid[12+j], None]
            for i in range(4):
                if stack[i] == 0:
                    stack.pop(i)
                    stack.insert(3,0)
            for i in range(4):
                if stack [i] == stack[i+1]:
                    stack [i] = stack[i]*2
                    score = score + stack[i]
                    stack[i+1] = 0
            for i in range(4):
                if stack [i] == 0:
                    stack.pop(i)
                    stack.insert(3,0)
            grid[0+j], grid[4+j], grid[8+j], grid[12+j] = stack[0], stack[1], stack[2], stack[3]
def right_left_calc(grid):
    global score
    for j in range(4):
            stack = [grid[0+j*4], grid[1+j*4], grid[2+j*4], grid[3+j*4]]
            for i in range(4):
                if stack[i] == 0:
                    stack.pop(i)
                    stack.insert(0,0)
            for i in range(3,-1,-1):
                if stack [i] == stack[i-1]:
                    stack [i] = stack[i]*2
                    score = score + stack[i]
                    stack[i-1] = 0
            for i in range(4):
                if stack [i] == 0:
                    stack.pop(i)
                    stack.insert(0, 0)
            grid[0+j*4], grid[1+j*4], grid[2+j*4], grid[3+j*4] = stack[0], stack[1], stack[2], stack[3]
def left_right_calc(grid):
    global score
    for j in range(4):
            stack = [grid[0+j*4], grid[1+j*4], grid[2+j*4], grid[3+j*4],None]
            for i in range(4):
                if stack[i] == 0:
                    stack.pop(i)
                    stack.insert(3,0)
            for i in range(4):
                if stack [i] == stack[i+1]:
                    stack [i] = stack[i]*2
                    score = score + stack[i]
                    stack[i+1] = 0
            for i in range(4):
                if stack [i] == 0:
                    stack.pop(i)
                    stack.insert(3, 0)
            grid[0+j*4], grid[1+j*4], grid[2+j*4], grid[3+j*4] = stack[0], stack[1], stack[2], stack[3]


def spawn_animation(next_bloc):
    global spawn_state
    global frame
    if spawn_state == True:
        if next_bloc == []:
            spawn_state = False
        else:
            spawn_cord = num_to_grid(next_bloc[0]+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0]+53-53/7*frame, bg_Y+ spawn_cord[1]+53-53/7*frame, 107*frame/7, 107*frame/7)
            pygame.draw.rect(WIN, num_to_color(next_bloc[1]), SQR,0,3)
            pygame.display.update()
            if frame == 7:
                spawn_state = False
                frame = 1
                grid[next_bloc[0]] = next_bloc[1]
                print (grid)
            else:
                frame = frame + 1

def spawn_next_bloc():
    if 0 in grid:
        next_bloc = pick_random(grid)
        return next_bloc
    else:
        print("shit")
        i = []
        return i

def check_if_won(grid):
    if 2048 in grid:
        global won
        global dog
        global pog
        won = True
    if won == True:
        if score > highscore:
            with open('highscore.json','w') as file:
                file.write(str(score))
        score = 0
        splash.set_alpha(dog)
        WIN.blit(splash, (-80,0))
        if dog < 140:
            dog = dog + 3
        if dog > 90:
            if pog < 600:
                pog = pog + 14
            WIN.blit(win_text, (-40,-600 + pog))



def draw_window(grid):
    global score
    WIN.fill((250,248,239))
    WIN.blit(background, (bg_X, bg_Y))

    for i in range(16): #display blocs
        if grid[i] == 2:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_2bloc(SQR)
        elif grid[i] == 4:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_4bloc(SQR)
        elif grid[i] == 8:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_8bloc(SQR)
        elif grid[i] == 16:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_16bloc(SQR)
        elif grid[i] == 32:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_32bloc(SQR)
        elif grid[i] == 64:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_64bloc(SQR)
        elif grid[i] == 128:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_128bloc(SQR)
        elif grid[i] == 256:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_256bloc(SQR)
        elif grid[i] == 512:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_512bloc(SQR)
        elif grid[i] == 1024:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_1024bloc(SQR)
        elif grid[i] == 2048:
            spawn_cord = num_to_grid(i+1)
            SQR = pygame.Rect(bg_X+ spawn_cord[0], bg_Y+ spawn_cord[1], 107, 107)
            draw_2048bloc(SQR)
    score_text = score_font.render(f"Score: {score}", 1, (25,5,5))
    text_rect = score_text.get_rect(center=(WIDTH/2+140, HEIGHT/2-190))
    WIN.blit(score_text, text_rect)
    highscore_text = highscore_font.render(f"highscore: {highscore}", 1, (25,5,5))
    hightext_rect = highscore_text.get_rect(center=(WIDTH/2-200, HEIGHT/2-170))
    WIN.blit(highscore_text, hightext_rect)
    WIN.blit(overlay, (0,0))
    if restart.draw(WIN):
            global won
            global running
            reset_grid()
            won = False
            running = False
            if score > highscore:
                with open('highscore.json','w') as file:
                    file.write(str(score))
            score = 0
            



def main():
    global spawn_state
    global next_bloc
    global running
    global grid
    global won
    global highscore
    running = True
    clock = pygame.time.Clock()

    with open('highscore.json','r') as file:
        readscore = int(file.read())
    if readscore == 0:
        highscore = 0
    else:
        highscore = readscore
    i = pick_random(grid)
    grid[i[0]] = i[1]
    i = pick_random(grid)
    grid[i[0]] = i[1]
    print (grid)

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if spawn_state == False:
                if won == False:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            up_down_calc(grid)
                            spawn_state = True
                            next_bloc = spawn_next_bloc()
                        elif event.key == pygame.K_DOWN:
                            down_up_calc(grid)
                            spawn_state = True
                            next_bloc = spawn_next_bloc()
                        elif event.key == pygame.K_LEFT:
                            left_right_calc(grid)
                            spawn_state = True
                            next_bloc = spawn_next_bloc()
                        elif event.key == pygame.K_RIGHT:
                            right_left_calc(grid)
                            spawn_state = True
                            next_bloc = spawn_next_bloc()

        draw_window(grid)
        spawn_animation(next_bloc)
        check_if_won(grid)
        pygame.display.update()
    main()

if __name__ == "__main__":
    main()
    