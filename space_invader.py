import pygame
import time
import random
pygame.font.init()

okno = pygame.display.set_mode((640, 480))

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)

    player_vel = 5

    obiekt = Obiekt(320, 480)

class Obiekt:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.obiekt_img = None

    def draw(self, window):
        pygame.draw.rect(self.obiekt_img, (self.x, self.y 10, 10))



    def redraw_window():
        okno.fill((0,0,0))
        lives_label = main_font.render(f"Lives:{lives}", 1,(255,255,255))

        okno.blit(lives_label, (20, 20))

        obiekt.draw(okno)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]and obiekt.x - player_vel > 0:
            obiekt.x -= player_vel
        if keys[pygame.K_d] and obiekt.x + player_vel + 20 < 640:
            obiekt.x += player_vel
        if keys[pygame.K_w] and obiekt.y - player_vel > 0:
            obiekt.y -= player_vel
        if keys[pygame.K_s] and obiekt.y + player_vel + 20 < 480:
            ship.y += player_vel


main()
