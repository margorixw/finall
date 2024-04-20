import pygame
from random import randint
pygame.init()


win_w = 600
win_h = 480
FPS = 40

window = pygame.display.set_mode((win_w, win_h))

class Button:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.transform.scale(image, (w, h))

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

play_img = pygame.image.load("btn.start.png")

btn_start = Button(win_w//2-100, (win_h-10)//2, 200, 50, play_img)

# pygame.mixer_music.load("space.ogg")
# pygame.mixer_music.set_volume(0.1)
# pygame.mixer_music.play(-1)

# fire_snd = pygame.mixer.Sound("fire.ogg")
# 
star_img = pygame.image.load("star.png")

class GameSprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Pers(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.clip = 5

    def move(self, key_left, key_right):
        k = pygame.key.get_pressed()
        if k[key_right]:
            if self.rect.bottom <= win_h:
                self.rect.y += self.speed 
        elif k[key_left]:
            if self.rect.y >= 0:
                self.rect.y -= self.speed
        if k[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
            
        # if self.clip > 0:
        # fire_snd.play()
            b = Bullet(self.rect.centerx, self.rect.y, 15, 20, star_img, 4)
            print (1)
            # self.clip -= 1
    def reload(self):
        if self.clip <= 0:
            self.clip = 5

class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        # self.direction = direction
        # self.x2 = x2
        # self.x1 = x
    
    def move(self):
        global lost
        self.rect.x -= self.speed
        if self.rect.x <= 0:
            lost += 1
            # print(lost)
            self.rect.x = randint(win_w, win_w+150)
            self.rect.y = randint(0, win_h-self.rect.h)
            self.speed = randint(1, 3)
            # print(self.rect.x, self.rect.y)

        

bullets = []
class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        bullets.append(self)
    
    def move(self):
        self.rect.x += self.speed
        if self.rect.x > 800:
            bullets.remove(self)
    
font1 = pygame.font.SysFont("Arial", 20)
font2 = pygame.font.SysFont("Arial", 50)

reload_alert = font1.render("Щоб перезарядитись, натисни E", True, (255, 0, 0))

window = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption("Shooter 0.1")
clock = pygame.time.Clock()

background = pygame.image.load("forest.jpg")
background = pygame.transform.scale(background, (win_w, win_h))
window.blit(background, (0, 0))


hero_img = pygame.image.load("ninjab.png")
hero = Pers(0, 400, 70, 80, hero_img, 5)

enemy_img = pygame.image.load("ninjar.png") 

enemies = []
for i in range(5):
    enemy = Enemy(randint(win_w, win_w+150), randint(0, win_h-70), 90, 70, enemy_img, randint(1, 3))
    enemies.append(enemy)

# record
with open("record.txt", "r", encoding="UTF-8") as file:
    record = int(file.read())

print(record)
def new_record(old, new):
    if new > old:
        with open("record.txt", "w", encoding="UTF-8") as file:
            file.write(str(new))  

           
screen = "menu"
score = 0
lost = 0
game = True
finish = False
while game:
    if screen == "menu":

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game = False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_start.rect.collidepoint(x, y):
                #click_snd.play()
                    screen = "play"
        window.fill((0,255,0))
        btn_start.reset()

    if screen == "play":

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game = False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_start.rect.collidepoint(x, y):
                    #click_snd.play()
                    screen = "menu"
        if not finish:
            window.blit(background, (0, 0))
            hero.update()
            hero.move(pygame.K_w, pygame.K_s)
            for enemy in enemies:
                enemy.update()
                enemy.move()
                if hero.rect.colliderect(enemy.rect):
                    finish = True
                    new_record(record, score)
                    game_over = font2.render("Game Over", True, (255, 0, 0))
                for bullet in bullets:
                    if bullet.rect.colliderect(enemy.rect):
                        score += 1
                        # print(score)
                        enemy.rect.x, enemy.rect.y = randint(win_w, win_w+150), randint(0, win_h-70)
                        bullets.remove(bullet)

            for bullet in bullets:
                bullet.update()
                bullet.move()
            if lost >= 3:
                finish = True
                game_over = font2.render("Game Over", True, (255, 0, 0))
                new_record(record, score)
        else:
            window.blit(game_over, (200,200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and finish:
                finish = False
                lost = 0
                score = 0
                hero.rect.x, hero.rect.y = 0, 400
                for enemy in enemies:
                    enemy.rect.x, enemy.rect.y = randint(win_w, win_w+150), randint(0, win_h-70)
           # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not finish:
              # hero.shoot()
           # elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and not finish:
             #   hero.reload()
        propusk = font1.render("Пропущено: "+str(lost), True, (255, 255, 255))
        window.blit(propusk, (10,10))
        killed = font1.render("Вбито: "+str(score), True, (255, 255, 255))
        window.blit(killed, (10,30))
        clip_stat = font1.render("Зарядів: "+str(hero.clip), True, (255, 255, 255))
        window.blit(clip_stat, (350,10))
        if hero.clip <= 0:
            window.blit(reload_alert, (300,30))
    pygame.display.update()
    clock.tick(FPS)