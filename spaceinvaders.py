import pygame
import os 
import time
import random

pygame.init()
pygame.font.init()

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH,HEIGHT))

bg_spaceinvaders = pygame.image.load('spaceinvadersbg.png')

#statki enemy
zielony_mob = pygame.image.load('enemystatek1.png')
niebieski_mob = pygame.image.load('enemystatek2.png')
zolty_mob = pygame.image.load('enemystatek3.png')

#statek gracza

gracz_statek = pygame.image.load('graczstatek.png')

#lasery
laser_przeciwnik = pygame.image.load('przeciwniklaser.png')
laser_gracz = pygame.image.load('graczlaser.png')

class Lasery():

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def rysuj(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def ruch(self, velocity):
        self.y += velocity
    
    def poza_ekranem(self, height):
        return not(self.y <= height and self.y >= 0)

    def kolizja(self, obiekt):
       return collide(self, obiekt) 



class Obiekt:
    cooldown = 15
    
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.obiekt_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0 

    def rysuj(self, window):
        window.blit(self.obiekt_img, (self.x, self.y))
        for laser in self.lasers:
            laser.rysuj(screen)

    def ruch_laserami(self, velocity, obiekt):
        self.cooldowns()
        for laser in self.lasers:
            laser.ruch(velocity)
            if laser.poza_ekranem(HEIGHT):
                self.lasers.remove(laser)
            elif laser.kolizja(obiekt):
                obiekt.health -= 10
                self.lasers.remove(laser)


    def cooldowns(self):
        if self.cooldown_counter >= self.cooldown:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:          
            self.cooldown_counter += 1

    def strzelanie(self):
        if self.cooldown_counter == 0:
            laser = Lasery(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def get_width(self):
        return self.obiekt_img.get_width()
    
    def get_height(self):
        return self.obiekt_img.get_height()



class Gracz(Obiekt):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.obiekt_img = gracz_statek
        self.laser_img = laser_gracz
        self.mask = pygame.mask.from_surface(self.obiekt_img)
        self.max_hp = health


    def ruch_laserami(self, velocity, obiekty):
        self.cooldowns()
        for laser in self.lasers:
            laser.ruch(velocity)
            if laser.poza_ekranem(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obiekt in obiekty:
                    if laser.kolizja(obiekt):
                        obiekty.remove(obiekt)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

class Wrogi_statek(Obiekt):
    mapka_kolorow = {"zielony":(zielony_mob, laser_przeciwnik), "niebieski":(niebieski_mob, laser_przeciwnik),"zolty":(zolty_mob, laser_przeciwnik)}

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.obiekt_img, self.laser_img = self.mapka_kolorow[color]
        self.mask = pygame.mask.from_surface(self.obiekt_img)
    
    def ruch(self, velocity):
        self.y += velocity

def collide(obiekt1, obiekt2):
    offset_x = obiekt2.x - obiekt1.x
    offset_y = obiekt2.y - obiekt1.y
    return obiekt1.mask.overlap(obiekt2.mask, (offset_x, offset_y)) != None

def space_invaders():
    run = True
    FPS = 60
    lives = 3
    main_font = pygame.font.SysFont("calibri", 30)

    wrogowie = []
    wave_lenght = 5
    enemy_vel = 4
    player_vel = 5 
    laser_vel = 8

    clock = pygame.time.Clock()

    gracz = Gracz(300, 400)

    przegrana = False

    def redraw_window():
        screen.blit(bg_spaceinvaders, (0,0))

        lives_label = main_font.render(f"Lives:{lives}", 1,(255,255,255))
        screen.blit(lives_label, (10,10))
        
        gracz.rysuj(screen)

        for wrog in wrogowie:
            wrog.rysuj(screen)


        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or gracz.health <=0:
            przegrana = True
            if przegrana == True:
                pygame.quit()

        if len(wrogowie) == 0:
            wave_lenght += 3
            for i in range(wave_lenght):
                wrog = Wrogi_statek(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["zielony", "niebieski", "zolty"]))
                wrogowie.append(wrog)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]and gracz.x - player_vel > 0:
            gracz.x -= player_vel
        if keys[pygame.K_RIGHT] and gracz.x + player_vel + gracz.get_width() < 640:
            gracz.x += player_vel
        if keys[pygame.K_UP] and gracz.y - player_vel > 0:
            gracz.y -= player_vel
        if keys[pygame.K_DOWN] and gracz.y + player_vel + gracz.get_height() < 480:
            gracz.y += player_vel
        if keys[pygame.K_SPACE]:
            gracz.strzelanie()

        for wrog in wrogowie[:]:
            wrog.ruch(enemy_vel)
            wrog.ruch_laserami(laser_vel, gracz)

            if random.randrange(0, 2*60) == 1:
                wrog.strzelanie()

            if wrog.y + wrog.get_height() > HEIGHT:
                lives -= 1
                wrogowie.remove(wrog)
        
        gracz.ruch_laserami(-laser_vel, wrogowie)




space_invaders()  