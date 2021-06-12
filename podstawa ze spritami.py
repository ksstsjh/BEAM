import pygame, sys

pygame.init()
pygame.display.set_caption("BEAM")

# screen & background
fps = 60



screen = pygame.display.set_mode((640,480))

background = pygame.image.load('castle.jpg')



### basic ustawienia dla drzwi 

door_width = 20
door_height = 100
door_X = 10
door_Y = 200

#rozwinelam tworzenie postaci - zamiast kwadrata spawni sie teraz sprite
#na razie jeszcze bez animacji bo dlugo mi zajelo ogarniecie zeby w ogole sprite sie pojawil i mozna bylo nim ruszac, ale teraz jak juz go mam to z gorki bedzie
#jutro dorzuce villaina, a na razie ide spac, baaaaaaaiii

class Gracz(pygame.sprite.Sprite):

    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.image = pygame.image.load('gemchar1.png')
       # okreslenie gdzie ma sie zespawnic
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
        

        

player=Gracz()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
player_width = 40
player_height = 50
playerX = 300 # spawnuje się przy wejściu na osi X
playerY = 400 # spawnuje się przy wejściu na osi Y

player_velocity = 10



### game loop

run = True
while run:
    pygame.time.delay(70)

    for event in pygame.event.get():        # żeby program prawidłowo się zamykał po naciśnięciu magicznego czerwonego guziczka
        if event.type == pygame.QUIT:
            run = False
        
        keys = pygame.key.get_pressed()

    



    screen.blit(background, (0,0)) # dzięki temu nie "rysujemy" naszym ruchem,, tylko gracz chodzi bez zostawiania śladu (wystarczy zakomentować tę linijkę żeby zobaczyć o co cho)
        
       
    door = pygame.draw.rect(screen, (255, 200, 255), (door_X, door_Y, door_width, door_height)) # narysowanie drzwi

# kolizja!!! teraz po zderzeniu z różowymi drzwiami gracz zmienia kolor na zielony, ale w domyśle w tym momencie kończy się obecny loop i zaczyna space invaders

    #collide = player.colliderect(door)
    #if collide:
        #player = pygame.draw.rect(screen, (0, 255, 0), (playerX, playerY, player_width, player_height))
    all_sprites.update() 
    all_sprites.draw(screen)
    pygame.display.flip()
    
    pygame.display.update()


pygame.quit()
