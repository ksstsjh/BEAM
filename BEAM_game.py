import pygame, sys

# init i inne pierdy dla formalności
pygame.init()
pygame.display.set_caption("BEAM")

# screen & background

screen = pygame.display.set_mode((640,480))

background = pygame.image.load('background.png')


### basic ustawienia dla postaci gracza

player_width = 40
player_height = 50
playerX = 300 # spawnuje się przy wejściu na osi X
playerY = 400 # spawnuje się przy wejściu na osi Y
player_velocity = 10



### basic ustawienia dla drzwi 

door_width = 20
door_height = 100
door_X = 10
door_Y = 200



### game loop

run = True
while run:
    pygame.time.delay(70)

    for event in pygame.event.get():        # żeby program prawidłowo się zamykał po naciśnięcieu magicznego czerwonego guziczka
        if event.type == pygame.QUIT:
            run = False
    
    ######
    ### sterowańsko 
    ######
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and playerX > player_velocity + 10: # fragmenty "and playerX > player_velocity + 10:" jest dla ustalenia granic pokoju
        playerX -= player_velocity
    if keys[pygame.K_RIGHT] and playerX < 600 - player_velocity - player_width:
        playerX += player_velocity
    if keys[pygame.K_UP] and playerY > player_velocity + 10:
        playerY -= player_velocity
    if keys[pygame.K_DOWN] and playerY < 440 - player_height - player_velocity:
        playerY += player_velocity


    screen.blit(background, (0,0)) # dzięki temu nie "rysujemy" naszym ruchem,, tylko gracz chodzi bez zostawiania śladu (wystarczy zakomentować tę linijkę żeby zobaczyć o co cho)
    player = pygame.draw.rect(screen, (255, 0, 0), (playerX, playerY, player_width, player_height)) # narysowanie gracza-prostokata
    door = pygame.draw.rect(screen, (255, 200, 255), (door_X, door_Y, door_width, door_height)) # narysowanie drzwi

# kolizja!!! teraz po zderzeniu z różowymi drzwiami gracz zmienia kolor na zielony, ale w domyśle w tym momencie kończy się obecny loop i zaczyna space invaders

    collide = player.colliderect(door)
    if collide:
        player = pygame.draw.rect(screen, (0, 255, 0), (playerX, playerY, player_width, player_height))



    pygame.display.update()



pygame.quit()
