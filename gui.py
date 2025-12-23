import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 300))

running = True
playing = False




def DrawText(text, location, size, color=(255,255,255)):

    font = pygame.font.Font(None, size)
    screen.blit(font.render(text, True, color), location)


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
        


    DrawText("Tux Macro", (15, 15), 32)
    DrawText("Pattern: CornerXSnake", (15, 50), 32)
    DrawText("F1: START", (15, 300 - 32 - 15), 32)
    DrawText("F3: STOP", (15 + 32 * 4, 300 - 32 - 15), 32)
    
    pygame.display.flip()
    clock.tick(30)

    return running, playing