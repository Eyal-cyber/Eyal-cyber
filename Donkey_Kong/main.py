import pygame, sys, random, math
from pygame.locals import *

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
#initalize pygame objects
pygame.init()
#declairing font
font = pygame.font.SysFont('Bold', 20)
#creating screen
win = pygame.display.set_mode((500, 500))
#header
pygame.display.set_caption("Donkey kong")

#pictuers
wall=pygame.image.load('wall.jpg')
bg=pygame.image.load('main_bg.jpg')
monkey=pygame.image.load('monkey.png')
ladder_img=pygame.image.load('ladder.png')
player_img=pygame.image.load('player.png')
ghost=pygame.image.load('dead.png')
toomb=pygame.image.load('tombstone.png')
victory_img=pygame.image.load('win.jpg')
#resize the image
monkey_image = pygame.transform.scale(monkey, (200,150))
wall_img = pygame.transform.scale(wall, (500,500))
background=pygame.transform.scale(bg,(500,500))
ladder_scaled=pygame.transform.scale(ladder_img,(250,300))
playerImg=pygame.transform.scale(player_img,(50,50))
victory=pygame.transform.scale(victory_img,(500,500))



#list to contain number of barrels
barrel_x = []
barrel_y = []
barrel_Img=[]
barrelspeed = []
barrels=6

#appending to list barrel location
for i in range(barrels):
    barrel_Img.append(pygame.image.load('barrel.png'))
    barrel_x.append(random.randint(0,160))
    barrel_y.append(80)
    barrelspeed.append(random.randint(4,20))

#draw enemy
def enemy(x,y,i):
    win.blit(barrel_Img[i],(x,y))
#draw player
def player(x,y):
    win.blit(playerImg,(x,y))
#draw ladder
def ladder(x,y):
    win.blit(ladder_scaled,(x,y))

#cheking for collision
def isCollision(barrel_x, barrel_y, playerx, playery):
    distance = math.sqrt(math.pow(barrel_x - playerx, 2) + (math.pow(barrel_y - playery, 2)))
    if distance < 27:
        return True
    else:
        return False


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

#set mouse click veriable
click = False

#menu
def main_menu():
    while True:
        win.fill((0,0,0))

        win.blit(background,(0,0))
        draw_text('Help', font, (255, 255, 255), win, 20, 330)
        draw_text('Start', font, (255, 255, 255), win, 20, 250)

        #mouse x and y
        mx, my = pygame.mouse.get_pos()

        start_button = pygame.Rect(60, 240, 100, 40)
        help_button = pygame.Rect(60, 320, 100, 40)
        if start_button.collidepoint((mx, my)):
            if click:
                game()
        if help_button.collidepoint((mx, my)):
            if click:
                Help()
        pygame.draw.rect(win, (0, 128, 0), start_button)
        pygame.draw.rect(win, (12, 24, 189), help_button)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


#game
def game():
    playerx = 10
    playery = 390
    health = 3
    width = 40
    height = 60
    speed = 10
    isJump = False
    jumpCount = 6.5
    run = True
    while run:
        pygame.time.delay(100)

        win.fill((0, 0, 0))

        win.blit(wall_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and playerx > speed:
            playerx -= speed

        if keys[pygame.K_RIGHT] and playerx < 500 - speed - width:
            playerx += speed

        #player on ladder or not
        if ((playerx == 340 or playerx == 350 or playerx == 360 or playerx == 370) and (playery <= 390 and not playery <= 280)) or (( playerx == 290 or playerx == 300 or playerx == 310 or playerx == 320) and playery <= 170 and playery != 60) or  ((playerx == 90 or playerx == 100 or playerx == 110 or playerx == 120) and( playery <= 280 and playery >= 180)):
            if keys[pygame.K_UP] and playery > speed:
                playery -= speed

            if keys[pygame.K_DOWN] and playery < 500 - height - speed:
                playery += speed

        if (playerx>420 and playery==280) or (playerx<20 and playery==170) or (playerx>440 and playery==60):
            playery+=110

        #jump
        if not (isJump):
            if keys[pygame.K_SPACE]:
                isJump = True
        else:
            if jumpCount >= -6.5:
                playery -= (jumpCount * abs(jumpCount)) * 0.5
                jumpCount -= 1
            else:
                jumpCount = 6.5
                isJump = False

        # always adding to the x position and when hitting boundris change direction
        for i in range(barrels):
            barrel_x[i] += barrelspeed[i]
            if barrel_x[i] <= 0:
                barrelspeed[i] = barrelspeed[i] * -1
                barrel_y[i] += 110
            elif barrel_x[i] >= 480:
                barrelspeed[i] = -barrelspeed[i]
                barrel_y[i] += 110
            elif barrel_x[i] <= barrelspeed[i] and barrel_y[i] >= 430:
                barrel_y[i] = 80
                barrel_x[i] = 55
                barrelspeed[i] = random.randint(4, 20)

            # collision

            collision = isCollision(barrel_x[i], barrel_y[i], playerx, playery)
            if collision and health > 0:
                health -= 1
                barrel_x[i] = random.randint(55, 80)
                barrel_y[i] = 80
            enemy(barrel_x[i], barrel_y[i], i)

        # check if player reached the gorilla(win)
        if playerx <= 10 and playery <= 80:
            pygame.mixer.music.load('victorysound.mp3')
            pygame.mixer.music.play(0)
            pygame.time.delay(900)
            Win()

        #death
        if health==0:
            pygame.mixer.music.load('game_over.mp3')
            pygame.mixer.music.play(0)
            health-=1
            pygame.time.delay(3000)
            Game_over()

        #draw the ladders,flors,player,monkey
        pygame.draw.rect(win, (255, 0, 0), (playerx, playery, 40, 8))
        pygame.draw.rect(win, (0, 255, 0), (playerx, playery, 50 - ((50 / 3) * (3 - health)), 8))
        pygame.draw.rect(win, (0, 0, 255), (0, 100, 450, 10))
        pygame.draw.rect(win, (0, 0, 255), (40, 210, 495, 10))
        pygame.draw.rect(win, (0, 0, 255), (0, 320, 450, 10))
        pygame.draw.rect(win, (0, 0, 255), (0, 430, 500, 10))
        player(playerx, playery)
        ladder(230, 60)
        ladder(20, 170)
        ladder(280, 280)

        win.blit(monkey_image, (-50, 0))
        pygame.display.update()

    pygame.quit()




#help screen
def Help():
    running = True
    while running:
        win.fill((0, 0, 0))
        win.blit(monkey_image, (-50, 0))
        #text
        draw_text('Help:', font, (255, 255, 255), win, 20, 20)
        draw_text('this is donkey kong game!!!!!',font,(255,255,255),win,30,250)
        draw_text('here are the rools:',font,(255,255,255),win,30,265)
        draw_text('the player need to reach the gorilla in order to win the game',font,(255,255,255),win,30,290)
        draw_text('the player can jump by pressing space bar',font,(255,255,255),win,30,305)
        draw_text('the player can go up and down using up and down arrows',font,(255,255,255),win,30,320)
        draw_text('but only on ladders', font, (255, 0, 0), win, 30, 335)
        draw_text('if you get hit by a barrel 3 times you die!!!',font,(255,255,255),win,30,370)
        draw_text('goodluck:)',font,(0,255,0),win,30,395)
        draw_text('escape to return to menu', font, (0, 120, 255), win, 30, 420)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)



#game over screen
def Game_over():
    running = True
    while running:
        win.fill((0, 0, 0))
        win.blit(ghost, (260, 50))
        win.blit(toomb, (200, 300))
        draw_text('YOU DIED',font, (255, 255, 255), win, 210, 140)
        draw_text('press A to play again press Q to quit', font, (255, 255, 255), win, 140, 200)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_a:
                    game()
                elif event.key ==K_q:
                    running=False
                    pygame.quit()

        pygame.display.update()



#victory screen
def Win():
    running=True
    while running:
        win.fill((0,0,0))
        win.blit(victory,(0,0))
        draw_text('YOU WON', font, (255, 255, 255), win, 210, 40)
        draw_text('press A to play again press Q to quit', font, (12, 255, 255), win, 140, 100)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_a:
                    game()
                elif event.key ==K_q:
                    running=False
                    pygame.quit()

        pygame.display.update()


main_menu()