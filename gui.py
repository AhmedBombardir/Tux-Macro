import pygame
import sys
import settings
import os

pygame.init()

#------------------------------------------------------------------
# FONT LOADING - DejaVu Sans Mono
#------------------------------------------------------------------

def LoadFont(size):
    """Load DejaVu Sans Mono from project folder or system"""
    # Try project folder first
    project_font = os.path.join('fonts', 'DejaVuSansMono.ttf')
    
    if os.path.exists(project_font):
        try:
            return pygame.font.Font(project_font, size)
        except:
            pass
    
    # Try system path
    system_font = '/usr/share/fonts/TTF/DejaVuSansMono.ttf'
    if os.path.exists(system_font):
        try:
            return pygame.font.Font(system_font, size)
        except:
            pass
    
    # Fallback to pygame default
    print(f"[GUI] DejaVu Sans Mono not found, using default font")
    return pygame.font.Font(None, size)

# Single font variable
FONT = LoadFont(12)
SMALL_FONT = LoadFont(10)

#------------------------------------------------------------------

clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 400))

running = True
playing = False

# ---------- Label class -----------

class Label:
    def __init__(self, text, font, color=(255, 255, 255)):
        self.text = text
        self.font = font
        self.color = color
        self.rect = pygame.Rect(0, 0, 0, 0)  # Pozycja będzie ustawiana przez Tab
    
    def draw(self, screen):
        rendered = self.font.render(self.text, True, self.color)
        screen.blit(rendered, (self.rect.x, self.rect.y))
    
    def handle_event(self, event):
        pass  # Labels don't handle events

# ---------- Dropdown class -----------

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


class TextBox:
    def __init__(self, x, y, width, height, font, placeholder="", on_submit = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.on_submit = on_submit
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if clicked inside
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False  # Unfocus on Enter
            else:
                # Add character
                self.text += event.unicode
    
    def draw(self, screen):
        # Background color - highlight if active
        color = (80, 80, 80) if self.active else (60, 60, 60)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (120, 120, 120), self.rect, 2)
        
        # Display text or placeholder
        display_text = self.text if self.text else self.placeholder
        text_color = (255, 255, 255) if self.text else (100, 100, 100)
        
        rendered = self.font.render(display_text, True, text_color)
        # Add some padding from left edge
        screen.blit(rendered, (self.rect.x + 5, self.rect.y + (self.rect.height - rendered.get_height()) // 2))
        
        # Draw cursor if active
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer % 60 < 30:  # Blink every 30 frames
                cursor_x = self.rect.x + 5 + self.font.size(self.text)[0]
                cursor_y = self.rect.y + 5
                pygame.draw.line(screen, (255, 255, 255), 
                               (cursor_x, cursor_y), 
                               (cursor_x, cursor_y + self.rect.height - 10), 2)


# ---------- Tab class -----------

class Tab:
    def __init__(self, name):
        self.name = name
        self.elements = []  # List of elements with their relative positions
        
    def add_element(self, element, rel_x, rel_y):
        """Add element with relative coordinates to tab content area"""
        self.elements.append({
            'element': element,
            'rel_x': rel_x,
            'rel_y': rel_y
        })
    
    def draw(self, screen, content_rect):
        """Draw all elements inside the content area"""
        for item in self.elements:
            elem = item['element']
            # Move element to proper position relative to content area
            elem.rect.x = content_rect.x + item['rel_x']
            elem.rect.y = content_rect.y + item['rel_y']
            elem.draw(screen)
    
    def handle_event(self, event, content_rect):
        """Pass events to all elements (with adjusted positions)"""
        for item in self.elements:
            elem = item['element']
            # Update position before handling event
            elem.rect.x = content_rect.x + item['rel_x']
            elem.rect.y = content_rect.y + item['rel_y']
            elem.handle_event(event)

# ---------- TabManager class -----------

class TabManager:
    def __init__(self, x, y, width, height, tab_bar_height=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.tab_bar_height = tab_bar_height
        self.tabs = []
        self.active_index = 0
        self.font = FONT
        
        # Calculate content area (below tab bar)
        self.content_rect = pygame.Rect(
            x, 
            y + tab_bar_height,
            width,
            height - tab_bar_height
        )
    
    def add_tab(self, tab):
        """Add a new tab to the manager"""
        self.tabs.append(tab)
    
    def draw(self, screen):
        """Draw tab bar and active tab content"""
        if not self.tabs:
            return
        
        # 1. Draw tab bar with tab names
        tab_width = self.rect.width / len(self.tabs)
        
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(
                self.rect.x + i * tab_width,
                self.rect.y,
                tab_width,
                self.tab_bar_height
            )
            
            # Highlight active tab
            color = (80, 80, 80) if i == self.active_index else (50, 50, 50)
            pygame.draw.rect(screen, color, tab_rect)
            pygame.draw.rect(screen, (120, 120, 120), tab_rect, 2)
            
            # Tab name
            text = self.font.render(tab.name, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=tab_rect.center))
        
        # 2. Draw content area background
        pygame.draw.rect(screen, (30, 30, 30), self.content_rect)
        pygame.draw.rect(screen, (120, 120, 120), self.content_rect, 2)
        
        # 3. Draw active tab content
        self.tabs[self.active_index].draw(screen, self.content_rect)
    
    def handle_event(self, event):
        """Handle tab switching and pass events to active tab"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if clicked on tab bar
            if self.rect.y <= event.pos[1] <= self.rect.y + self.tab_bar_height:
                if self.rect.x <= event.pos[0] <= self.rect.x + self.rect.width:
                    tab_width = self.rect.width / len(self.tabs)
                    clicked_index = int((event.pos[0] - self.rect.x) / tab_width)
                    
                    if 0 <= clicked_index < len(self.tabs):
                        self.active_index = clicked_index
                        print(f"[GUI] Switched to tab: {self.tabs[clicked_index].name}")
                        return  # Don't pass event further
        
        # Pass event to active tab
        if self.tabs:
            self.tabs[self.active_index].handle_event(event, self.content_rect)


def DrawText(text, location, size, color=(255,255,255)):
    """Draw text using FONT at specified size"""
    font = pygame.font.Font('/usr/share/fonts/TTF/DejaVuSansMono.ttf', size)
    screen.blit(font.render(text, True, color), location)

#------------------------------------------------------------------
# CALLBACK FUNCTIONS - Update settings when dropdown changes
#------------------------------------------------------------------

def OnPatternChange(pattern_name):
    """Called when pattern dropdown changes"""
    settings.pattern = pattern_name
    print(f"[GUI] Pattern changed to: {pattern_name}")

def OnFieldChange(field_name):
    """Called when field dropdown changes"""
    settings.field = field_name
    print(f"[GUI] Field changed to: {field_name}")

def OnSprinklerChange(sprinkler_name):
    """Called when sprinkler dropdown changes"""
    settings.sprinkler = sprinkler_name
    print(f"[GUI] sprinkler changed to: {sprinkler_name}")

def OnTextSubmit(text):
    try:
        # Convert to float and validate
        value = float(text)
        if value > 0:
            settings.moveSpeed = value
            print(f"[GUI] Movespeed set to: {value}")
        else:
            print(f"[GUI] Invalid movespeed: must be positive")
    except ValueError:
        print(f"[GUI] Invalid movespeed: '{text}' is not a number")

#------------------------------------------------------------------
# CREATE DROPDOWNS
#------------------------------------------------------------------

pattern_dropdown = Dropdown(
    x=0, y=0, width=85, height=15,  # Position will be relative to tab content
    options=["CornerXSnake", "E_lol", "Stationary"],
    font=SMALL_FONT,
    on_change=OnPatternChange
)

field_dropdown = Dropdown(
    x=0, y=0, width=85, height=15,  # Position will be relative to tab content
    options=["Dandelion", "Clover", "Sunflower", "Mushroom", "Blue Flower", 
             "Strawberry", "Spider", "Bamboo", "Pineapple", "Stump", 
             "Pine Tree", "Pumpkin", "Cactus", "Rose", "Mountain", "Coconut", "Pepper"],
    font=SMALL_FONT,
    on_change=OnFieldChange
)

sprinkler_dropdown = Dropdown(15, 30, 85, 15,
options=["Basic", "Silver", "Golden", "Diamond", "Supreme"],
font=SMALL_FONT, on_change=OnSprinklerChange)

# Set initial values from settings
pattern_dropdown.selected = settings.pattern
field_dropdown.selected = settings.field


#------------------------------------------------------------------
# CREATE TABS AND TAB MANAGER
#------------------------------------------------------------------

# Create tab manager
tab_manager = TabManager(x=10, y=40, width=480, height=360, tab_bar_height=30)


# ---------- Gather Tab ----------
gather_tab = Tab("Gather")

pattern_label = Label("Pattern:", FONT)
gather_tab.add_element(pattern_dropdown, rel_x=280, rel_y=30)

field_label = Label("Field:", FONT)
gather_tab.add_element(field_dropdown, rel_x=380, rel_y=30)

gather_tab.add_element(pattern_label, rel_x=280, rel_y=10)
gather_tab.add_element(field_label, rel_x=380, rel_y=10)



# ---------- Collect Tab -----------
collect_tab = Tab("Collect")

wip_label = Label("Work In Progress...", FONT, color=(150, 150, 150))
collect_tab.add_element(wip_label, 15, 15)



# ---------- Kill Tab -----------
kill_tab = Tab("Kill")
kill_tab.add_element(wip_label, 15, 15)



# ---------- Boost Tab -----------
boost_tab = Tab("Boost")
boost_tab.add_element(wip_label, 15, 15)



# ---------- Planters Tab -----------
planters_tab = Tab("Planters")
planters_tab.add_element(wip_label, 15, 15)



# ---------- Settings Tab -----------
settings_tab = Tab("Settings")
sprinkler_label = Label("Sprinkler", FONT)
movespeed_label = Label("Movespeed", FONT)
textbox = TextBox(
    x=15, y=60, 
    width=120, height=20, 
    font=FONT,
    placeholder="Enter text...",
    on_submit=OnTextSubmit
)

textbox.text = str(settings.moveSpeed)

settings_tab.add_element(sprinkler_label, 15, 20)
settings_tab.add_element(sprinkler_dropdown, 15, 35)
settings_tab.add_element(movespeed_label, 15, 60)
settings_tab.add_element(textbox, 15, 75)



# ---------- Credits Tab -----------
credits_tab = Tab("Credits")
credits_tab.add_element(wip_label, 15, 15)



# Add tabs to manager
tab_manager.add_tab(gather_tab)
tab_manager.add_tab(collect_tab)
tab_manager.add_tab(kill_tab)
tab_manager.add_tab(boost_tab)
tab_manager.add_tab(planters_tab)
tab_manager.add_tab(settings_tab)
tab_manager.add_tab(credits_tab)

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
                print(f"[GUI] Macro {status}")
                print(f"[GUI] Current settings: Pattern={settings.pattern}, Field={settings.field}")

            if event.key == pygame.K_F3:
                running = False

        # Handle tab manager events (includes dropdown handling)
        tab_manager.handle_event(event)

    if not running:
        pygame.quit()
        sys.exit()

    screen.fill("black")

    #------------------------------------------------------------------
    # Draw UI elements
    #------------------------------------------------------------------

    DrawText("Tux Macro", (10, 10), 24)
    
    # Show current status
    status_color = (0, 255, 0) if playing else (255, 255, 255)
    status_text = "RUNNING" if playing else "IDLE"
    #DrawText(f"Status: {status_text}", (15, 60), 24, status_color)
    #DrawText(f"Pattern: {settings.pattern}", (15, 85), 20)
    #DrawText(f"Field: {settings.field}", (15, 100), 20)

    # Draw tab manager (with all tabs and dropdowns)
    tab_manager.draw(screen)

    DrawText("F1: START/STOP", (15, 400 - 16 - 15), 12)
    DrawText("F3: EXIT", (140, 400 - 16 - 15), 12)

    #------------------------------------------------------------------

    pygame.display.flip()
    clock.tick(30)

    return running, playing