from pygame import Surface, display, draw, font, key, sprite, event, QUIT, init, time
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP
from random import randrange
from time import sleep

init()
App = display.set_mode([660, 700])

WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLACK = [0, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]

class Player(sprite.Sprite):
    length = []
    def __init__(self):
        super().__init__()
        self.player = Surface([60, 60])
        self.player.fill(BLUE)
        self.rect = self.player.get_rect()
        self.rect.x = 300
        self.rect.y = 300
        self.state = 'ready'

    def move(self):
        Key = key.get_pressed()

        if Key[K_UP]:
            if self.state != 'DOWN':
                self.state = 'UP'

        if Key[K_DOWN]:
            if self.state != 'UP':
                self.state = 'DOWN'
            
        if Key[K_RIGHT]:
            if self.state != 'LEFT':
                self.state = 'RIGHT'

        if Key[K_LEFT]:
            if self.state != 'RIGHT':
                self.state = 'LEFT'

        if self.state == 'UP':
            self.rect.y -= 60

        if self.state == 'DOWN':
            self.rect.y += 60

        if self.state == 'RIGHT':
            self.rect.x += 60

        if self.state == 'LEFT':
            self.rect.x -= 60

        if self.rect.x > 630:
            self.rect.x = 0

        if self.rect.x < 0:
            self.rect.x = 600

        if self.rect.y > 630:
            self.rect.y = 0

        if self.rect.y < 0:
            self.rect.y = 600

class Enemy(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.enemy = Surface([60, 60])
        self.enemy.fill(GREEN)
        self.rect = self.enemy.get_rect()
        self.rect.x = randrange(0, 660, 60)
        self.rect.y = randrange(0, 660, 60)

    def reset_rect(self):
        self.rect.x = randrange(0, 660, 60)
        self.rect.y = randrange(0, 660, 60)

class Tail(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tail = Surface([60, 60])
        self.tail.fill(BLUE)
        self.rect = self.tail.get_rect()
        self.rect.x = -250
        self.rect.y = -250

Snake = Player()
Food = Enemy()
Food_Group = sprite.Group()
Food_Group.add(Food)

Game_font = font.SysFont('Times', 20)
Score_count = 0
Score = Game_font.render('Score: {}'.format(Score_count), True, RED)

SnakeTail = sprite.Group()

clock = time.Clock()
fps = 10

running = True
while running:
    clock.tick(fps)
    Snake.move()
    App.fill(BLACK)

    App.blit(Score, [0, 670])
    App.blit(Food.enemy, Food.rect)
    App.blit(Snake.player, Snake.rect)

    for i in Snake.length:
        App.blit(i.tail, i.rect)

    for i in range(1, 16):
        draw.line(App, RED, [60 * i, 0], [60 * i, 660])

    for i in range(1, 16):
        draw.line(App, RED, [0, i * 60], [660, i * 60])
        
    if sprite.spritecollide(Snake, Food_Group, False):
        Food.reset_rect()
        Score_count += 1
        Score = Game_font.render('Score: {}'.format(Score_count), True, RED)
        NewTail = Tail()
        SnakeTail.add(NewTail)
        Snake.length.append(NewTail)

    if sprite.spritecollide(Snake, SnakeTail, False):
        Snake.length = []
        Snake.state = 'stop'
        Snake.rect.x = 300
        Snake.rect.y = 300
        Score_count = 0
        Score = Game_font.render('Score: {}'.format(Score_count), True, RED)
        sleep(2)

    for i in range(len(Snake.length) - 1, 0, -1):
        x = Player.length[i - 1].rect.x
        y = Player.length[i - 1].rect.y
        Player.length[i].rect.x = x
        Player.length[i].rect.y = y

    if len(Snake.length) > 0:
        x = Snake.rect.x
        y = Snake.rect.y
        Player.length[0].rect.x = x
        Player.length[0].rect.y = y

    for i in event.get():
        if i.type == QUIT:
            running = False
            
    display.update()

quit()