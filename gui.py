import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 300))

running = True
playing = False

def Render():
    global running, playing  # TO JEST KLUCZOWE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                playing = not playing
                print(f"Game: {playing}")
            if event.key == pygame.K_F3:
                running = False

    if not running:
        pygame.quit()
        sys.exit()

    screen.fill("black")
    # Opcjonalnie: zmiana koloru tła, gdy makro działa
    if playing:
        screen.fill((0, 100, 0)) # Ciemnozielony gdy działa
        
    pygame.display.flip()
    clock.tick(30)

    return running, playing