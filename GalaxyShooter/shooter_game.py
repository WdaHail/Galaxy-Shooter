from pygame import *
from random import randint



font.init()
font = font.SysFont('Times New Roman', 36)
win = font.render("You Won!", True, (250, 250, 250))
lose = font.render("You Lost.", True, (250, 250, 250))
#loseexit = font.render("You Lost.", True, (250, 250, 250))
exiting = font.render("Exiting Program in 3 sec", True, (250, 250, 250))
noevent = font.render("Модификатор: Никакой", True, (250, 250, 250))
swarmevent = font.render("Модификатор: Улей", True, (250, 250, 250))
bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global keys
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 50:
            self.rect.y += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 4)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1



win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
clock = time.Clock()
FPS = 60

img_back = "galaxy.jpg"

background = transform.scale(image.load(img_back), (win_width, win_height))

#Музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
bulletfire = mixer.Sound('fire.ogg')
#Создание спрайтов
player = Player('rocket.png', 5, win_height - 100, 80, 100, 10)
bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 5, 8, 4)
aliens = sprite.Group()

for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    aliens.add(monster)

#переменные
run = True
finish = False
score = 0
lost = 0
goal = 10
max_lost = 3
level = 1
randevent = randint(1,2)

#Игровой цикл
while run:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                bulletfire.play()
                player.fire()

    if finish == False:
        window.blit(background, (0, 0))
        task_text = font.render("Сбейте " + str(goal) + ' кораблей.', 1, (255, 255, 255))
        score_text = font.render("Счёт: " + str(score), 1, (255, 255, 255))        
        lost_text = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))       
        level_text = font.render("Уровень: " + str(level), 1, (255, 255, 255))

        player.update()
        aliens.update()

        player.reset()
        aliens.draw(window)

        bullets.update()
        bullets.draw(window)
        window.blit(task_text, (300, 15))
        window.blit(score_text, (10, 20))
        window.blit(lost_text, (10, 50))
        window.blit(level_text, (10, 80))
        if sprite.spritecollide(player, aliens, False) or lost >= 3:
            window.blit(lose, (350, 250))
            finish = True
            level -= 2
            if level < 1:
                window.blit(exiting, (350, 350))                
                run = False
                print('You Lost')

        collides = sprite.groupcollide(aliens, bullets, True, True)

        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            aliens.add(monster)  

        #if level >= 2:
        #    randevent = randint(1,2)
        #    if randevent == 1:
        #        window.blit(swarmevent, (500, 540))
        #        for i in range(1, 2):
        #            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
        #            aliens.add(monster)
        #    if randevent == 2:
        #        window.blit(noevent, (500, 500))

        if score >= goal:
            window.blit(win, (350, 250))
            finish = True
            level += 1
            goal += randint(3, 7)
        display.update()
    else:
        finish = False
        score = 0
        lost = 0                
        for b in bullets:
            b.kill()
        for m in aliens:
            m.kill()    

        time.delay(3000)

        for i in range(1, 6):
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            aliens.add(monster)
        if level >= 6:
            for i in range(1, 8):
                monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
                aliens.add(monster)
        
        display.update()




        