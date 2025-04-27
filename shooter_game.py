from pygame import *
from random import randint 

Window = display.set_mode((700,500))
display.set_caption("Шутер")
d = transform.scale(image.load("galaxy.jpg"), (700, 500))
Window.blit(d, (0,0))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
rwe = mixer.Sound('Fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_with, player_hide, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_with, player_hide))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        Window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20, 15)
        bullets.add(bullet)

sprite1 = Player('rocket.png', 310,435, 65, 65,15)

finish = False
lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >=  500:
            self.rect.y = 0
            self.rect.x = randint(0,700)
            lost+= 1
 
enemy1 = Enemy('ufo.png', 435,0, 65, 65, 10)
enemy2 = Enemy('ufo.png', 356, 0,  65, 65, 8)
enemy3 = Enemy('ufo.png', 333, 0, 65, 65, 6)
enemy4 = Enemy('ufo.png', 267, 0, 65, 65,  8)
enemy5 = Enemy('ufo.png', 235, 0, 65, 65, 6)


Enemy_group = sprite.Group()
Enemy_group.add(enemy1)
Enemy_group.add(enemy2)
Enemy_group.add(enemy3)
Enemy_group.add(enemy4)
Enemy_group.add(enemy5)

bullets = sprite.Group()


font.init()
font1 = font.Font(None, 36)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

score = 0
font2 = font.Font(None, 70)
win = font2.render('Ты победил:', 1,(255, 255, 255))
lose = font2.render('ты проиграл:', 1, (189, 51, 164))
run = True
while run:
    
    if finish != True:
        Window.blit(d, (0,0))
        text = font1.render('Пропушено:'+ str(lost), 1,(255, 255, 255))
        text2 = font1.render('счет:'+ str(lost), 1,(255, 255, 255))
        
        Window.blit(text, (10,10))
        sprite1.reset()
        sprite1.update()
        Enemy_group.update()
        Enemy_group.draw(Window)
        bullets.draw(Window)
        bullets.update()
        sprites_list = sprite.groupcollide( Enemy_group, bullets, True, True)
        for i in sprites_list: 
            enemy = Enemy ('ufo.png', 195, 0, 65, 65, 10)
            Enemy_group.add(enemy)
            score += 1 
        if score >= 10:
            finish = True
            Window.blit(win, (45, 89))
        if lost >= 10:
            finish = True
            Window.blit(lose, (34, 67))

          

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                sprite1.fire()
                rwe.play()
    display.update()