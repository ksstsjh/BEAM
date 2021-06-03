import pygame, sys, config

# init i inne pierdy dla formalności
pygame.init()
pygame.display.set_caption("BEAM")

# screen & background

screen = pygame.display.set_mode((640,480))

background = pygame.image.load('background.png')


# player

player_image = pygame.image.load('player_img.png')
player_width = 40
player_height = 50
playerX = 300 # spawnuje się przy wejściu na osi X
playerY = 400 # spawnuje się przy wejściu na osi Y
player_velocity = 8




# game loop

run = True
while run:
    pygame.time.delay(70)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and playerX > player_velocity + 25:
        playerX -= player_velocity
    # if keys[pygame.K_LEFT] and playerX < 620 - player_velocity - player_width:
    #     playerX -= player_velocity

    if keys[pygame.K_RIGHT] and playerX < 620 - player_velocity - player_width:
        playerX += player_velocity
    if keys[pygame.K_UP] and playerY > player_velocity + 25:
        playerY -= player_velocity
    if keys[pygame.K_DOWN] and playerY < 460 - player_height - player_velocity:
        playerY += player_velocity


    screen.blit(background, (0,0)) # dzięki temu nie "rysujemy" naszym ruchem,, tylko gracz chodzi bez zostawiania śladu (wystarczy zakomentować tę linijkę żeby zobaczyć o co cho)
    pygame.draw.rect(screen, (255, 0, 0), (playerX, playerY, player_width, player_height))
    pygame.display.update()



pygame.quit()
