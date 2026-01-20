import pygame
import sys
import settings


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 400))

running = True
playing = False

class Dropdown:
    
    def __init__(self, x, y, width, height, options, font, on_change=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.font = font
        self.selected = options[0]
        self.open = False
        self.on_change = on_change  # Callback when selection changes

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
                        old_selected = self.selected
                        self.selected = opt
                        self.open = False
                        
                        # Call callback if selection changed
                        if old_selected != self.selected and self.on_change:
                            self.on_change(self.selected)
                        break
                else:
                    self.open = False

    def draw(self, screen):
        # Main box
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
# CALLBACK FUNCTIONS - Update settings when dropdown changes
#------------------------------------------------------------------

def OnPatternChange(pattern_name):
    """Called when pattern dropdown changes"""
    settings.pattern = pattern_name
    print(f" Pattern changed to: {pattern_name}")

def OnFieldChange(field_name):
    settings.field = field_name
    print(f"[GUI] Field changed to: {field_name}")


#------------------------------------------------------------------
# DROPDOWNS WITH CALLBACKS
#------------------------------------------------------------------

pattern_dropdown = Dropdown(
    x=250, y=80, width=80, height=15,
    options=["CornerXSnake", "E_lol", "Stationary"],
    font=pygame.font.Font(None, 15),
    on_change=OnPatternChange  # Link callback
)

field_dropdown = Dropdown(
    x=350, y=80, width=80, height=15,
    options=["Dandelion", "Clover", "Sunflower", "Mushroom", "Blue Flower", 
             "Strawberry", "Spider", "Bamboo", "Pineapple", "Stump", 
             "Pine Tree", "Pumpkin", "Cactus", "Rose", "Mountain", "Coconut", "Pepper"],
    font=pygame.font.Font(None, 15),
    on_change=OnFieldChange  # Link callback
)

# Set initial values from settings
pattern_dropdown.selected = settings.pattern
field_dropdown.selected = settings.field

#------------------------------------------------------------------

def Render():
    global running, playing

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                playing = not playing
                status = "STARTED" if playing else "STOPPED"
                print(f" Macro {status}")
                print(f" Current settings: Pattern={settings.pattern}, Field={settings.field}")

            if event.key == pygame.K_F3:
                running = False

        pattern_dropdown.handle_event(event)
        field_dropdown.handle_event(event)

    if not running:
        pygame.quit()
        sys.exit()

    screen.fill("black")

    field_dropdown.draw(screen)
    pattern_dropdown.draw(screen)

    #------------------------------------------------------------------

    DrawText("Tux Macro", (15, 15), 48)
    DrawText("Pattern", (250, 55), 24)
    DrawText("Field", (350, 55), 24)
    
    # Show current status
    status_color = (0, 255, 0) if playing else (255, 255, 255)
    status_text = "RUNNING" if playing else "IDLE"
    DrawText(f"Status: {status_text}", (15, 80), 24, status_color)

    DrawText("F1: START", (15, 400 - 32 - 15), 32)
    DrawText("F3: STOP", (15 + 32 * 4, 400 - 32 - 15), 32)

    #------------------------------------------------------------------

    pygame.display.flip()
    clock.tick(30)

    return running, playing