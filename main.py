import pygame 
import random

from pyparsing import White

#initialization of all functions in pygame and mixer for the audio
pygame.init()
pygame.mixer.init() 

#display stuff
WIDTH = 600
HEIGHT = 750
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Afloat")
clock = pygame.time.Clock()
FPS = 60 

#intialization for game display the borders 
WHITE=(255,255,255)
GREY=(212,210,212)
BLACK=(0,0,0)
BLUE=(0,97,148)
RED=  (162,8,8)
ORANGE = (183, 119, 0)
GREEN = (0, 127, 33)
YELLOW = (197, 199, 37)

#no of balls and velocity of them 
score = 0
velocity = 4

paddle_width = 124
paddle_height = 15


#sprite class used to combine image and rect/sounds/animations etc 
#implies sprite object is a representation of a real object in the game 

all_sprites_list = pygame.sprite.Group()

wall_width = 16

paddle_sound = pygame.mixer.Sound('sounds/sounds_paddle.wav')
wall_sound = pygame.mixer.Sound('sounds/sounds_wall.wav')

class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def moveRight(self, pixels):
        self.rect.x += pixels
        if self.rect.x > WIDTH - wall_width - paddle_width:
            self.rect.x = WIDTH - wall_width - paddle_width

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < wall_width:
            self.rect.x = wall_width

class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height, vx, vy):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.velocity = [vx, vy]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = self.velocity[0]
        self.velocity[1] = -self.velocity[1]

#intialization of objects 
paddle = Paddle(WHITE, paddle_width, paddle_height)
paddle.rect.x = WIDTH // 2 - paddle_width // 2
paddle.rect.y = HEIGHT - 65

ball_1 = Ball(BLUE, 10, 10, random.randint(2,5),random.randint(2,5))
ball_1.rect.x= WIDTH //random.randint(2,6) - random.randint(2,10)
ball_1.rect.y = HEIGHT//5 - 5

ball_2 = Ball(RED, 10, 10,random.randint(2,5),random.randint(2,5))
ball_2.rect.x= WIDTH //random.randint(2,6) - random.randint(2,10)
ball_2.rect.y = HEIGHT//5 - 5

ball_3 = Ball(GREEN, 10, 10,random.randint(2,5),random.randint(2,5))
ball_3.rect.x= WIDTH //random.randint(2,6) - random.randint(2,10)
ball_3.rect.y = HEIGHT//5 - 5



balls_list=[ball_1,ball_2,ball_3]

balls = len(balls_list)

all_sprites_list.add(paddle)
for ball in balls_list:
    all_sprites_list.add(ball)


def main(score, balls):

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #ann output
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.moveLeft(10)
        if keys[pygame.K_RIGHT]:
            paddle.moveRight(10)

        all_sprites_list.update()
        for ball in balls_list:
            if ball.rect.y < 40:
                ball.velocity[1] = -ball.velocity[1]
                wall_sound.play()

            if ball.rect.x >= WIDTH - wall_width - 10:
                ball.velocity[0] = -ball.velocity[0]
                wall_sound.play()

            if ball.rect.x <= wall_width:
                ball.velocity[0] = -ball.velocity[0]
                wall_sound.play()

            if ball.rect.y > HEIGHT:
                balls -= 1
                if balls == 0:
                    font = pygame.font.Font('text/Caviar_Dreams_Bold.ttf', 70)
                    text = font.render("GAME OVER", 1, WHITE)
                    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                    screen.blit(text, text_rect)
                    pygame.display.update()
                    pygame.time.wait(2000)
                    run = False
            #store the x,y and pass it 
            if pygame.sprite.collide_mask(ball, paddle):
                ball.rect.x += ball.velocity[0]
                ball.rect.y -= ball.velocity[1]
                ball.bounce()
                paddle_sound.play()

        screen.fill(BLACK) 

    

        pygame.draw.line(screen, YELLOW, [0, 19], [WIDTH, 19], 40)
        pygame.draw.line(screen, YELLOW, [(wall_width / 2) - 1, 0], [(wall_width / 2) - 1, HEIGHT], wall_width)
        pygame.draw.line(screen, YELLOW, [(WIDTH - wall_width / 2) - 1, 0], [(WIDTH - wall_width / 2) - 1, HEIGHT], wall_width)

        pygame.draw.line(screen, BLACK, [(wall_width / 2) - 1, HEIGHT - 65 + paddle_height / 2 - 54 / 2], [(wall_width / 2) - 1, HEIGHT - 65 + paddle_height / 2 - 54 / 2 + 54], wall_width)
        pygame.draw.line(screen, BLACK, [(WIDTH - wall_width / 2) - 1, HEIGHT - 65 + paddle_height / 2 - 54 / 2], [(WIDTH - wall_width / 2) - 1, HEIGHT - 65 + paddle_height / 2 - 54 / 2 + 54], wall_width)


        all_sprites_list.draw(screen)

        pygame.display.update() 
        
        clock.tick(FPS)

    pygame.quit()


main(score, balls)
