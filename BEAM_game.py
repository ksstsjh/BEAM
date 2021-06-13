import pygame, sys

# init i inne pierdy dla formalności
pygame.init()
pygame.display.set_caption("BEAM")

# screen & background

screen = pygame.display.set_mode((640,480))

walkUp = [pygame.image.load('gemchar4.png'), pygame.image.load('gemchar4.1.png'), pygame.image.load('gemchar4.2.png')]
walkDown = [pygame.image.load('gemchar1.png'), pygame.image.load('gemchar1.1.png'), pygame.image.load('gemchar1.2.png')]
walkRight = [pygame.image.load('gemchar2.png'), pygame.image.load('gemchar2.1.png'), pygame.image.load('gemchar2.2.png')]
walkLeft = [pygame.image.load('gemchar3.png'), pygame.image.load('gemchar3.1.png'), pygame.image.load('gemchar3.2.png')]

bg = pygame.image.load('castle.jpg')
player = pygame.image.load('gemchar1.png')

clock = pygame.time.Clock()

### basic ustawienia dla postaci gracza

player_width = 64
player_height = 64
playerX = 300 # spawnuje się przy wejściu na osi X
playerY = 400 # spawnuje się przy wejściu na osi Y
player_velocity = 5


### basic ustawienia dla drzwi 

door_width = 20
door_height = 130
door_X = 10
door_Y = 170

up = False
down = False
left = False
right = False
walkCount = 0

def redrawGameWindow():
    global walkCount

    screen.blit(bg, (0, 0))
    if walkCount + 1  >= 27:
        walkCount = 0

    if left:
        screen.blit(walkLeft[walkCount//9], (playerX,playerY))
        walkCount += 1

    elif right:
        screen.blit(walkRight[walkCount//9], (playerX,playerY))
        walkCount += 1

    elif up:
        screen.blit(walkUp[walkCount//9], (playerX,playerY))
        walkCount += 1

    elif down:
        screen.blit(walkDown[walkCount//9], (playerX,playerY))
        walkCount += 1

    else:
        screen.blit(player, (playerX,playerY))
        walkCount = 0

    pygame.display.update()


### game loop

run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():        # żeby program prawidłowo się zamykał po naciśnięcieu magicznego czerwonego guziczka
        if event.type == pygame.QUIT:
            run = False
    
    ######
    ### sterowańsko 
    ######
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and playerX > player_velocity + 10: # fragmenty "and playerX > player_velocity + 10:" jest dla ustalenia granic pokoju
        playerX -= player_velocity
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and playerX < 640 - player_velocity - player_width:
        playerX += player_velocity
        right = True
        left = False
    elif keys[pygame.K_UP] and playerY > player_velocity + 10:
        playerY -= player_velocity
        up = True
        down = False
    elif keys[pygame.K_DOWN] and playerY < 480 - player_height - player_velocity:
        playerY += player_velocity
        down = True
        up = False

    else:
        up = False
        down = False
        right = False
        left = False
        walkCount = 0

    redrawGameWindow()

#Gdzieś po tym miejscy zaczyna się problem xD bo, żeby sama postać nie była zasłoniona przez ten kwadrat, but also pokazuje jakiś problem przy colliderect :/ samo chodzenie i postać działa jeżeli to co jest poniżej jest zakomentowane
"""
    screen.blit(background, (0,0)) # dzięki temu nie "rysujemy" naszym ruchem,, tylko gracz chodzi bez zostawiania śladu (wystarczy zakomentować tę linijkę żeby zobaczyć o co cho)
    player = pygame.draw.rect(screen, (255, 0, 0), (playerX, playerY, player_width, player_height)) # narysowanie gracza-prostokata
    door = pygame.draw.rect(screen, (255, 200, 255), (door_X, door_Y, door_width, door_height)) # narysowanie drzwi

# kolizja!!! teraz po zderzeniu z różowymi drzwiami gracz zmienia kolor na zielony, ale w domyśle w tym momencie kończy się obecny loop i zaczyna space invaders

    collide = player.colliderect(door)
    if collide:
        player = pygame.draw.rect(screen, (0, 255, 0), (playerX, playerY, player_width, player_height))



    pygame.display.update()
"""


pygame.quit()
