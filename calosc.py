#blagam, niech ktos na to zerknie, bo jak wchodzi sie w drzwi to mi sie crashuje python calkowicie
#probowalam polaczyc wszystko ze soba i zrobilam mini title screen, ale zmiana loopa mi nie wychodzi totalnie
#jak sie osobno odpali wszystko to smiga cudnie, tak samo jak sie odpali tylko title screen i space invaders lub title screen i pierwszy stage z chodzeniem po zamku
#ale przejscie z zamku na space invaders przy kolizji sie wykrzacza totalnie i nie wiem jak mam to naprawić

import random
import pygame, sys, math
import os, time

pygame.init()
pygame.font.init()
pygame.display.set_caption("BEAM")

# screen & background
fps = 60

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH,HEIGHT))

background = pygame.image.load('castle.jpg')

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

### basic ustawienia dla drzwi 
door_width = 20
door_height = 100
door_X = 10
door_Y = 200

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
    run2 = True
    FPS = 60
    lives = 3
    main_font = pygame.font.SysFont("calibri", 30)

    wrogowie = []
    global wave_lenght
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
        while run2:
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
                    run2 = False

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



class Postac(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 10
        self.image = pygame.image.load('gemchar1.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = 300
        self.rect.bottom = 400
        
        
   
   #przerzucilam movement do klasy, bo inaczej mi nie smigalo 
    def update(self):
        self.speedx=0
        self.speedy=0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx=-10
        if keystate[pygame.K_RIGHT]:
            self.speedx=10
        if keystate[pygame.K_UP]:
            self.speedy=-10
        if keystate[pygame.K_DOWN]:
            self.speedy=10
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    #zeby nasz sprite nie uciekal poza ekran
        if self.rect.right > 620:
            self.rect.right = 620
        if self.rect.left < 15:
            self.rect.left = 15
        if self.rect.bottom > 445:
            self.rect.bottom = 445
        if self.rect.top < 25:
            self.rect.top = 25
        
    
    def kolizja(self, obiekt):
        return collide(self, obiekt)


class villain1(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('zombie1.1.png')
        self.rect=self.image.get_rect()
        self.rect.centerx = 80
        self.rect.bottom = 420
        self.counter = 0 
        

    def move(self):
        speed = 5
        distance = 50
        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed 
        elif self.counter >= distance and self.counter <= distance*2:
            self.rect.x -= speed
        else: 
            self.counter = 0 
        
        self.counter+=1


class villain2(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('zombie1.1.png')
        self.rect=self.image.get_rect()
        self.rect.centerx = 80
        self.rect.bottom = 220
        self.counter = 0 
        

    def move(self):
        speed = 8
        distance = 50
        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed 
        elif self.counter >= distance and self.counter <= distance*2:
            self.rect.x -= speed
        else: 
            self.counter = 0 
        
        self.counter+=1

class villain3(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('zombie1.1.png')
        self.rect=self.image.get_rect()
        self.rect.centerx = 80
        self.rect.bottom = 100
        self.counter = 0 
        

    def move(self):
        speed = 6
        distance = 50
        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed 
        elif self.counter >= distance and self.counter <= distance*2:
            self.rect.x -= speed
        else: 
            self.counter = 0 
        
        self.counter+=1

enemy1=villain1(80,420)
enemy2=villain2(80,220)
enemy3=villain3(80,100)
enemy_list = pygame.sprite.Group()
enemy_list.add(enemy1)
enemy_list.add(enemy2)
enemy_list.add(enemy3)

### game loop

def main():

    player=Postac()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    player_width = 40
    player_height = 50
    playerX = 300 # spawnuje się przy wejściu na osi X
    playerY = 400 # spawnuje się przy wejściu na osi Y
    player_velocity = 10

    run = True
    while run:
        pygame.time.delay(70)

        for event in pygame.event.get():        # żeby program prawidłowo się zamykał po naciśnięciu magicznego czerwonego guziczka
            if event.type == pygame.QUIT:
                run = False
        
            keys = pygame.key.get_pressed()


        screen.blit(background, (0,0)) # dzięki temu nie "rysujemy" naszym ruchem,, tylko gracz chodzi bez zostawiania śladu (wystarczy zakomentować tę linijkę żeby zobaczyć o co cho)
        
       
        door = pygame.draw.rect(screen, (255, 200, 255), (door_X, door_Y, door_width, door_height)) # narysowanie drzwi


#tu sie dzieja zle rzeczy - zostawilam na ostatnim podejsciu do tego, bo juz nawet nie pamietam jak pierwotnie to wygladalo 
        if player.rect.colliderect(door) == True:
            run2 = True
            while run2:
                space_invaders()

        
        #if player.rect.colliderect(enemy_list):
            #player.kill()
            #pygame.quit()

        all_sprites.update() 
        all_sprites.draw(screen) 
        enemy_list.draw(screen)
        for e in enemy_list:
            e.move()
   
        pygame.display.flip()
        pygame.display.update()


bg_title = pygame.image.load('titlescreen.png')

def menu():
    title_font = pygame.font.SysFont("calibri", 50, bold=True, italic=False)
    run = True 
    while run:
        screen.blit(bg_title, (0,0))
        title_label = title_font.render("PLAY", 1, (255,0,0))
        screen.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                
    

menu()

pygame.quit()
