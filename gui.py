import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 400))

running = True
playing = False


class Dropdown:
    
    def __init__(self, x, y, width, height, options, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.font = font
        self.selected = options[0]
        self.open = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
            elif self.open:
                for i, opt in enumerate(self.options):
                    opt_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + (i + 1) * self.rect.height,
                        self.rect.width,
                        self.rect.height
                    )
                    if opt_rect.collidepoint(event.pos):
                        self.selected = opt
                        self.open = False
                        break
                else:
                    self.open = False

    def draw(self, screen):
        # main box
        pygame.draw.rect(screen, (60, 60, 60), self.rect)
        pygame.draw.rect(screen, (120, 120, 120), self.rect, 2)

        text = self.font.render(self.selected, True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=self.rect.center))

        if self.open:
            for i, opt in enumerate(self.options):
                opt_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + (i + 1) * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )
                pygame.draw.rect(screen, (40, 40, 40), opt_rect)
                pygame.draw.rect(screen, (120, 120, 120), opt_rect, 1)

                txt = self.font.render(opt, True, (255, 255, 255))
                screen.blit(txt, txt.get_rect(center=opt_rect.center))


def DrawText(text, location, size, color=(255,255,255)):
    font = pygame.font.Font(None, size)
    screen.blit(font.render(text, True, color), location)



#------------------------------------------------------------------

pattern_dropdown = Dropdown(
    x=100, y=60, width=80, height=15,
    options=["CornerXSnake", "E_lol", "Stationary"],
    font=pygame.font.Font(None, 15)
)

field_dropdown = Dropdown(
    x=100, y=60 + 32, width=80, height=15,
    options=["Dandelion", "Clover", "Sunflower", "Mushroom", "Blue Flower"],
    font=pygame.font.Font(None, 15)
)

#------------------------------------------------------------------

def Render():
    global running, playing, dropdown

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                playing = not playing
                print(f"Game: {playing}")

            if event.key == pygame.K_F3:
                running = False

        pattern_dropdown.handle_event(event)
        field_dropdown.handle_event(event)

    if not running:
        pygame.quit()
        sys.exit()

    screen.fill("black")

    pattern_dropdown.draw(screen)
    field_dropdown.draw(screen)

    #------------------------------------------------------------------

    DrawText("Tux Macro", (15, 15), 48)

    DrawText("Pattern: ", (15, 60), 24)
    DrawText("Field: ", (15, 60 + 32), 24)

    DrawText("F1: START", (15, 400 - 32 - 15), 32)
    DrawText("F3: STOP", (15 + 32 * 4, 400 - 32 - 15), 32)

    #------------------------------------------------------------------

    # change color when macro is running
    #if playing:
        #screen.fill((0, 100, 0))  # when working


    

    pygame.display.flip()
    clock.tick(30)

    return running, playing