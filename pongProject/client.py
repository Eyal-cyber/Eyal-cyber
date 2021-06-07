import pygame
import Database
from network import Network
from player import Player

width = 500
height = 500
ball_speed_x = 3
ball_speed_y = 3
COLOR = (188, 79, 131)
# create rect in the middle
ball = pygame.Rect(width / 2 - 15, height / 2 - 15, 30, 30)
# create screen
win = pygame.display.set_mode((width, height))
# screen name
pygame.display.set_caption("Client")
# initializes the variables
pygame.init()
# declaring font
font = pygame.font.SysFont('Bold', 30)
font1 = pygame.font.SysFont('Bold', 50)
font3 = pygame.font.Font('freesansbold.ttf', 70)
player1_score = 0
player2_score = 0



def drawgame(win, player, player2):
    global player1_score, player2_score
    # paint the screen white
    win.fill((0, 0, 0))
    # if both players connected, print them
    if player.connected() and player2.connected():
        player.draw(win)
        player2.draw(win)
        # draw ball
        pygame.draw.ellipse(win, COLOR, ball)
        score_text = font.render("Score: " + str(player2_score), True, (255, 200, 255))
        # text lable, represent on the screen
        win.blit(score_text, (0, 20))
        score_text2 = font.render("Score: " + str(player1_score), True, (255, 200, 255))
        win.blit(score_text2, (410, 20))

    # check win
    if player1_score == 5:
        win.fill((0, 0, 0))
        player1_win = font1.render("player 1 wins ", True, (255, 200, 255))
        win.blit(player1_win, (200, 250))

    elif player2_score == 5:
        win.fill((0, 0, 0))
        player2_win = font1.render(" player 2 wins", True, (255, 200, 255))
        win.blit(player2_win, (200, 250))

    pygame.display.update()


# ball movement
def ball_animation(player, player2):
    global ball_speed_x, ball_speed_y, player1_score, player2_score

    if player.connected() and player2.connected():
        # move the ball right down
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= height:
            # if the ball touch the screen, change direction
            ball_speed_y *= -1

        if ball.left <= 0:
            # check if ball hit one of the sides and delay the return of the ball
            pygame.time.delay(200)
            ball.x, ball.y = 250, 250
            ball_speed_x *= -1
            player1_score += 1


        if ball.right >= width:
            # check if hits player1 side and add score to player2 + delay the return of the ball
            pygame.time.delay(200)
            ball.x, ball.y = 250, 250
            ball_speed_x *= -1
            player2_score += 1

        if player1_score == 5 or player2_score == 5:
            ball.x,ball.y = 250,250
            ball_speed_x,ball_speed_y =0,0


        if ball.colliderect(player) or ball.colliderect(player2):
            # if the ball touch the screen, change direction
            ball_speed_x *= -1


def menu():
    running = True
    while running:
        pygame.display.set_caption("menu")
        text1 = font.render("press s to start  ", True, (255, 200, 255))
        text2 = font.render("press e to exit   ", True, (255, 200, 255))
        text3 = font3.render("ONLINE PONG  ", True, (255, 200, 255))

        win.blit(text1, (0, 120))
        win.blit(text2, (0, 140))
        win.blit(text3, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.quit()
                elif event.key == pygame.K_s:
                    main()
                    running = False

        pygame.display.update()


def loginscreen():
    global name,last_name,email
    pygame.display.set_caption("login screen")
    base_font = pygame.font.Font(None, 32)
    # gets and put into the date base
    user_name = ''
    user_lastname = ''
    user_email = ''
    color1_active = pygame.Color('lightskyblue3')
    color1_disable = pygame.Color('gray15')
    color2_active = pygame.Color('lightskyblue3')
    color2_disable = pygame.Color('gray15')
    color3_active = pygame.Color('lightskyblue3')
    color3_disable = pygame.Color('gray15')
    input_name = pygame.Rect(220, 115, 140, 32)
    input_lastname = pygame.Rect(220, 195, 140, 32)
    input_email = pygame.Rect(220, 275, 140, 32)
    start_button = pygame.Rect(200, 370, 100, 40)
    color1 = color1_active
    color2 = color2_active
    color3 = color3_active
    name_active = False
    lastname_active = False
    email_active = False
    mx, my = pygame.mouse.get_pos()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # if click on the rectangle
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_name.collidepoint(event.pos):
                    # if clicked the name rect, the color change
                    name_active = True
                    lastname_active = False
                    email_active = False
                elif input_lastname.collidepoint(event.pos):
                    # if clicked the last name rect, the color change
                    lastname_active = True
                    email_active = False
                    name_active = False
                elif input_email.collidepoint(event.pos):
                    # if clicked the email rect, the color change
                    email_active = True
                    name_active = False
                    lastname_active = False
                elif start_button.collidepoint(event.pos):
                    win.fill((0, 0, 0))
                    # gets the information for the database
                    name, last_name, email = user_name, user_lastname, user_email
                    Database.add_record(name,last_name,email)
                    Database.show_all()
                    menu()

                else:
                    email_active = False
                    name_active = False
                    lastname_active = False
            # enter name,lastname and email
            if event.type == pygame.KEYDOWN:
                if name_active == True:
                    # gets the key that been pressed
                    if event.key == pygame.K_BACKSPACE:
                        # cut the last char
                        user_name = user_name[0:-1]
                    else:
                        user_name += event.unicode
                    # if press on space disable.
                    if event.key == pygame.K_SPACE:
                        # get out of the rect
                        name_active = False

                elif lastname_active == True:
                    # gets the key that been pressed
                    if event.key == pygame.K_BACKSPACE:
                        user_lastname = user_lastname[0:-1]
                    else:
                        user_lastname += event.unicode
                    # if press on space disable.
                    if event.key == pygame.K_SPACE:
                        # get out of the rect
                        lastname_active = False

                elif email_active == True:
                    # gets the key that been pressed
                    if event.key == pygame.K_BACKSPACE:
                        user_email = user_email[0:-1]
                    else:
                        user_email += event.unicode
                    # if press on space disable.
                    if event.key == pygame.K_SPACE:
                        # get out of the rect
                        email_active = False

            win.fill((0, 0, 0))
            # firstname box
            if name_active:
                # if clicked the color change
                color1 = color1_active
            else:
                color1 = color1_disable
            # lastname box
            if lastname_active:
                color2 = color2_active
            else:
                color2 = color2_disable
            # email box
            if email_active:
                color3 = color3_active
            else:
                color3 = color3_disable
# render --> show the font
            text1 = font.render("Enter your name:", True, (255, 200, 255))
            text2 = font.render("Enter last name:", True, (255, 200, 255))
            text3 = font.render("Enter email address:", True, (255, 200, 255))
            text4 = font1.render("Login:", True, (255, 200, 255))
            text5 = font.render("Submit:", True, (255, 200, 255))
            win.blit(text1, (0, 120))
            win.blit(text2, (0, 200))
            win.blit(text3, (0, 280))
            win.blit(text4, (200, 40))
            win.blit(text5, (120, 380))

            pygame.draw.rect(win, (0, 128, 0), start_button)
            pygame.draw.rect(win, color1, input_name, 2)
            pygame.draw.rect(win, color2, input_lastname, 2)
            pygame.draw.rect(win, color3, input_email, 2)
            text_surface = base_font.render(user_name, True, (255, 255, 255))
            text_surface1 = base_font.render(user_lastname, True, (255, 255, 255))
            text_surface2 = base_font.render(user_email, True, (255, 255, 255))
            win.blit(text_surface, (input_name.x + 5, input_name.y + 5))
            win.blit(text_surface1, (input_lastname.x + 5, input_lastname.y + 5))
            win.blit(text_surface2, (input_email.x + 5, input_email.y + 5))

            # make the text box 100 in minimum
            input_name.w = max(100, text_surface.get_width() + 10)
            input_lastname.w = max(100, text_surface1.get_width() + 10)
            input_email.w = max(100, text_surface2.get_width() + 10)

            pygame.display.update()


def main():
    global player1_score, player2_score
    run = True
    n = Network()
    # player position
    p = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if (p.connected() and p2.connected()):
            ball_animation(p, p2)
            drawgame(win, p, p2)
            p.move()
            if player1_score == 5 or player2_score == 5:
                pygame.time.delay(300)
                run=False
                pygame.quit()



loginscreen()
