from pygame import *
from random import randint
import time as time_module

window = display.set_mode((700, 500))
display.set_caption('стрелялка')

background = transform.scale(image.load('galaxy (2).jpg'), (700, 500))

mixer.init()
mixer.music.load("space (3).ogg")
mixer.music.play(-1)


class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, speed, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 5
        if key_pressed[K_RIGHT] and self.rect.x < 700 - self.width - 5:
            self.rect.x += 5
    def fire(self):
        bullet = Bullet("bullet.png", -15, self.rect.centerx, self.rect.top,  15, 20)
        bullets.add(bullet)


lost = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - self.width - 5)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 40)



monster1 = Enemy("ufo.png", randint(2, 5), randint(0, 700 - 160 - 5), 0, 65, 55)
monster2 = Enemy("ufo.png", randint(2, 5), randint(0, 700 - 160 - 5), 0, 65, 55)
monster3 = Enemy("ufo.png", randint(2, 5), randint(0, 700 - 160 - 5), 0, 65, 55)
monster4 = Enemy("ufo.png",randint(2, 5), randint(0, 700 - 160 - 5), 0, 65, 55)
monster5 = Enemy("ufo.png", randint(2, 5), randint(0, 700 - 160 - 5), 0, 65, 55)

monsters = sprite.Group()

monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

asteroid1 = Enemy("asteroid.png", randint(2, 5), randint(0, 700 - 160 - 5), 0, 65, 55)
asteroid2 = Enemy("asteroid.png", randint(2, 5), randint(0, 700 - 160 - 5), 0, 65, 55)
asteroid3 = Enemy("asteroid.png", randint(2, 5), randint(0, 700 - 160 - 5), 0, 65, 55)

asteroids = sprite.Group()

asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)


bullets = sprite.Group()


rocket = Player("rocket.png", 10, 300, 400, 60, 80)

fire = mixer.Sound('fire.ogg')


finish = False

num_fire = 0

'''asteroid = transform.scale(image.load('asteroid.png'))
packet = transform.scale(image.load('ракета.png'))
bullet = transform.scale(image.load('пуля.png'))
ufo = transform.scale(image.load('ufo.png'))'''

clock = time.Clock()
FPS = 60

win = font2.render('you win!', True, (255, 255, 255))
lose = font2.render('you lose!', True, (255, 255, 255))

relote = font2.render('Wait, reload...', True, (255, 255, 255))

rel_time = 0

game = True
while game:

    if finish != True:

        window.blit(background, (0, 0))

        if num_fire >= 5 and rel_time == True:
            new_time = time_module.time()
            if new_time - last_time < 3:
                window.blit(relote, (300, 450))
            else:
                num_fire = 0
                rel_time = False

        rocket.reset()
        rocket.update()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        if sprite.spritecollide(rocket, monsters, False):
            finish = True
            window.blit(lose, (200,200))

        if sprite.spritecollide(rocket, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprites_list:
            score += 1
            monster1 = Enemy("ufo.png", randint(2, 5), randint(0, 700 - 160 - 5), 0, 65, 55)
            monsters.add(monster1)


        text_lost = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        window.blit(text_lost, (5, 5))

        text_score = font1.render('Счёт: ' + str(score), True, (255, 255, 255))
        window.blit(text_score, (5, 35))

        if score >= 3:
            finish = True
            window.blit(win, (200,200))
        if lost >= 15:
            finish = True
            window.blit(lose, (200,200))

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    rocket.fire()
                    num_fire += 1
                if num_fire >= 5:
                    rel_time = True
                    last_time = time_module.time()

    display.update()
    clock.tick(FPS)
