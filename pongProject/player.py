import pygame


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        # speed --> down
        self.vel = 5
        # speed --> up
        self.reverse_vel = 5
        self.ready = False

    def draw(self, win):
        # draw the player
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        # move the players
        keys = pygame.key.get_pressed()
        # if the player gets to the top of the window allowing going only down
        if self.y <= 0:
            self.reverse_vel = 0
        else:
            if keys[pygame.K_UP]:
                self.reverse_vel = 5
                self.y -= self.reverse_vel

        # if the player gets to the bottom of the window allowing going only up
        if self.y + 130 >= 500:
            self.vel = 0
        else:
            if keys[pygame.K_DOWN]:
                self.vel = 5
                self.y += self.vel

        self.update()

    def update(self):
        # update the player place
        self.rect = (self.x, self.y, self.width, self.height)

    def connected(self):
        # if player connected
        return self.ready
