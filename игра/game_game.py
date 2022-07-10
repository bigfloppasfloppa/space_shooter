from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def  __init__(self, player_image, xcor, ycor, widht, height, speed1, speed2):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (widht, height))
        self.speed1 = speed1
        self.speed2 = speed2
        self.rect = self.image.get_rect()
        self.rect.x = xcor
        self.rect.y = ycor

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed1

        if keys[K_DOWN] and self.rect.y < 395:
            self.rect.y += self.speed1

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed1

        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed1
    def fire(self):
        bullet = Bullet(bullet_image, self.rect.right, self.rect.top, 15, 20, 15, 0)
        bullets.add(bullet)
        bullet = Bullet(bullet_image, self.rect.left, self.rect.top, 15, 20, 15, 0)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        switch = randint(0,11)

        if switch % 2 == 0:
            direction = "left"
        else:
            direction = "right"

        if direction == "left":
            self.rect.y += self.speed1
            self.rect.x -= self.speed2
        else:
            self.rect.y += self.speed1
            self.rect.x += self.speed2

        global lost

        if self.rect.y > 450:
            self.rect.x = randint(80, 620)
            self.rect.y = randint(-5, 0)
            lost = lost + 1
            self.speed1 = randint(10,15)
            self.speed2 = randint(10,15)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed1
        #исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()

font.init()
font_stat = font.SysFont("Times New Roman", 36) # шрифт статистики
font_end = font.SysFont("Times New Roman", 80) # шрифт подведения итогов
lose_text = font_end.render("ТИ ПРОИГРАВ", True, (200, 25, 25))
win_text = font_end.render("ТИ ВЫИГРАВ", True, (0, 200, 0))

mixer.init()
mixer.music.load("music.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(loops=-1)
shot = mixer.Sound("fire.ogg")
lose = mixer.Sound("lose.mp3")
win = mixer.Sound("win.mp3")
kick = mixer.Sound("kick.mp3")

window = display.set_mode((700,500))
background = transform.scale(image.load("fon.jpg"), (700,500))

timer = time.Clock()
finish = False
game = True
lost = 0
score = 0
max_lost = 15 # макс. кол-во пропущенных врагов
max_score = 15 # макс. кол-во сбитых врагов 
life_points = 15 # очки жизни
level = 1 # уровень
victory = False # переменная-флаг перехода на следующий уровень
boss_life = 5 # здоровье врага


player_image = "rocket.png"
asteroid_image = "asteroid.png"
enemy_image = "ufo.png"
bullet_image = "bullet.png"
boss_image = "boss.png"

player = Player(player_image, 350, 450, 80, 100, 10, 0)
boss = Enemy(boss_image, randint(20, 680), randint(-15, 0), 50, 50, 5, 5)

enemies = sprite.Group()
for i in range(1,(6 * level)):
    enemy = Enemy(enemy_image, randint(20, 680), randint(-15, 0), 50, 50, 10, 10)
    enemies.add(enemy)

bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               shot.play()
               player.fire()

               player.fire()


    if not finish:        
        window.blit(background, (0,0))

        player.update()
        enemies.update()
        bullets.update()
        boss.update()

        player.reset()
        boss.reset()

        enemies.draw(window)
        bullets.draw(window) 

        text_win = font_stat.render("Счет: " + str(score), 1, (255, 0, 255))
        window.blit(text_win, (10, 20))

        text_lose = font_stat.render("Пропущено: " + str(lost), 1, (127, 45, 254))
        window.blit(text_lose, (10, 50))

        if sprite.spritecollide(player, enemies, False):
            sprite.spritecollide(player, enemies, False)
            kick.set_volume(6)
            kick.play()
            life_points -= 1

        if sprite.spritecollide(boss, bullets, False):
            sprite.spritecollide(boss, bullets, False)
            boss_life -= 1
            if boss_life == 0:
                boss.kill()    

        collisions = sprite.groupcollide(bullets, enemies, True, True)
        for collision in collisions:
            score += 1
            enemy = Enemy(enemy_image, randint(20, 680), randint(-5, 0), 50, 50, 10, 10)
            enemies.add(enemy)

        if score >= max_score:
            win.play()
            victory = True
            finish = True # цикл не останавливается, но
            # -> игра заканчивается
            window.blit(win_text, (100, 200))

        if lost >= max_lost or life_points == 0:
            lose.play()
            finish = True # цикл не останавливается, но
            # -> игра заканчивается
            window.blit(lose_text, (100, 200))


        if life_points > 10 and life_points <= 15:
            life_color = (0, 255, 0)
        elif life_points > 5 and life_points <= 10:
            life_color = (255, 255, 0)
        else:
            life_color = (255, 0, 0)

        text_life = font_stat.render("Жизни: " + str(life_points), 1, life_color)
        window.blit(text_life, (525, 20))

        text_level = font_stat.render("Уровень: " + str(level), 1, (255, 255, 255))
        window.blit(text_level, (525, 50))

        display.update()

    else:
        if victory == True:
            victory = False
            finish = False
            score = 0
            lost = 0
            life_points = 15
            level += 1
            for b in bullets:
                b.kill()
            for e in enemies:
                e.kill()
            time.delay(1000)
            for i in range(1,(6 * level)):
                enemy = Enemy(enemy_image, randint(20, 680), randint(-15, 0), 50, 50, 10, 10)
                enemies.add(enemy)
        else:
            finish = False
            score = 0
            lost = 0
            level = 1
            life_points = 15
            for b in bullets:
                b.kill()
            for e in enemies:
                e.kill()
            time.delay(1000)
            for i in range(1,6):
                enemy = Enemy(enemy_image, randint(20, 680), randint(-15, 0), 50, 50, 10, 10)
                enemies.add(enemy)

    time.delay(50)

'''
1. Идея
2. Планирование
3. Реализация (кодинг)
4. Тестирование
5. Выпуск (релиз)
6. Поддержка (support)
'''

# тестирование - попытка сломать программу

# дистрибуция - готовое решение для деплоя
# деплой - размещение решения на площадке