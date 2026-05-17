from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if (keys[K_UP])and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 155:
            self.rect.y += self.speed
    
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 155:
            self.rect.y += self.speed


back = (200, 255, 255)
win_height = 500
win_width = 800
window = display.set_mode((win_width, win_height))

game = True
finish = False
clock = time.Clock()
FPS = 60

ball_skins = ['tenis_ball.png', 'basketball_ball.png', 'golf_ball.png']


mixer.init()

table_kick = mixer.Sound("tk.ogg")
rocet_kick = mixer.Sound("rk.ogg")

mixer.music.load('dapstep.ogg')
mixer.music.play(-1)


racket1 = Player('racket.png', 30, 200, 10, 50, 150)
racket2 = Player('racket.png', win_width-80, 200, 10, 50, 150)

ball = GameSprite(ball_skins[randint(0, len(ball_skins) - 1)], randint(175, 225), randint(175, 225), 4, 50, 50)


font.init()
font = font.Font(None, 35)

lose1 = font.render('PLAYER 1 LOSE', True, (100, 0, 0))
lose2 = font.render('PLAYER 2 LOSE', True, (100, 0, 0))


rand_speed = [-1, 1]


speed_x = 3 * rand_speed[randint(0,1)]
speed_y = 3 * rand_speed[randint(0,1)]

score1 = 0
score2 = 0

background = transform.scale(image.load('background.jpg'), (win_width, win_height))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not(finish):
        window.blit(background, (0, 0))

        racket1.update_l()
        racket2.update_r()

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        score_board = font.render(f"{score1} : {score2}", True, (255, 255, 255))
        window.blit(score_board, (374, 20))

        if score1 >= 3 or score2 >= 3:
            finish = True
            if score1 >= 3:
                window.blit(lose2, (300, 200))
            else:
                window.blit(lose1, (300, 200))

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            rocet_kick.play()
        
        if ball.rect.y < 0 or ball.rect.y > win_height - 50:
            speed_y *= -1
            table_kick.play()
        

        if ball.rect.x < 0:
            score2 += 1
            ball.rect.x = randint(175, 225)
            ball.rect.y = randint(175, 225)
        
        if ball.rect.x > win_width - 50:
            score1 += 1
            ball.rect.x = randint(175, 225)
            ball.rect.y = randint(175, 225)

        racket1.reset()
        racket2.reset()
        ball.reset()
    
    display.update()
    clock.tick(FPS)
