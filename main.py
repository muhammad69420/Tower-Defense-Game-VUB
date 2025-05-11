import pygame
import math



pygame.init()

print("Starting game")

# Set up the display
WIDTH, HEIGHT = 960, 640
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")

from assets import load_image, tower_images, enemy_images, game_map_1, UI_images
from tower import Tower
from enemy import Enemy
from assets import level_data
from wavemanager import LevelManager
from assets import tower_stats
from assets import game_map_1


level_manager = LevelManager(level_data)



# clock
clock = pygame.time.Clock()
FPS = 180  #reduce FPS to 40 for gameplay, 180 for testing

# set up image
TILE_SIZE = 64
map = game_map_1
map = pygame.transform.scale(map, (WIDTH, HEIGHT))

Reached = False

def load_frames_from_sheet(path, num_frames):
    sheet = pygame.image.load(path).convert_alpha()
    frame_width = sheet.get_width() // num_frames
    frame_height = sheet.get_height()
    return [sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(num_frames)]


coin_icon = pygame.image.load("assets/coin_image.jpg")
coin_icon = pygame.transform.scale(coin_icon, (24, 24))

global font
font = pygame.font.Font(None, 20)

def write(text, location, color=(255, 255, 255)):
    WINDOW.blit(font.render(text, True, color), location)

# Functie om muispositie naar grid te converteren
def get_grid_position(mouse_x, mouse_y):
    grid_x = (mouse_x // TILE_SIZE) * TILE_SIZE
    grid_y = (mouse_y // TILE_SIZE) * TILE_SIZE
    return (grid_x, grid_y)

# object enemy
enemy_image = pygame.image.load("assets/Enemy.png")
path = [(0, 32), (736, 32), (736, 256), (96, 256), (96, 512), (960, 512)]

class Bases:
    def __init__(self, x, y, image, health):
        self.x = x
        self.y = y
        self.image = image
        self.health = health

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

base_image = pygame.image.load("assets/base1.png")
base = Bases(832, 480, base_image, health=10)
baseCoordinatesX = 896
baseCoordinatesY = 512

base_enemy = pygame.image.load("assets/EnemySpawn.png")
Spawn = Bases(0, 0, base_enemy, health=100000)

# Dit zijn de paden waar de vijand loopt - op deze tiles kan geen toren worden geplaatst
path_tiles = []
for x, y in path:
    # Voeg alle tiles die het pad vormen toe
    grid_x = (x // TILE_SIZE) * TILE_SIZE
    grid_y = (y // TILE_SIZE) * TILE_SIZE
    path_tiles.append((grid_x, grid_y))

  

#waarom een klasse voor coins?

"""
#class coins:  
    def __init__(self, start_amount, generation_rate):    
        self.amount = start_amount
        self.generation_rate = generation_rate
        self.last_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_time

        if elapsed_time >= 1000:
            self.amount += self.generation_rate
            self.last_time = current_time

coins = coins(100, 10)

# coin icon toevoegen
coin_icon = pygame.image.load("coin_image.jpg")
coin_icon = pygame.transform.scale(coin_icon, (24, 24))
"""
coins = 100
last_coin_time = pygame.time.get_ticks()




class menu:    #geen nut op een klasse van te maken?
    def __init__(self, x, y, width, height):
        # de rechthoek van het menu
        self.rect = pygame.Rect(x, y, width, height)
        # Menu begint verborgen
        self.visible = False
        
        # Stel de toren-opties in met hun posities en kosten
        self.tower_options = [
        {
        "name": "tower1",
        "price": 100,
        "button": pygame.Rect(x + 10, y + 40, width - 20, 30)
        },
        {
        "name": "tower2",
        "price": 150,
        "button": pygame.Rect(x + 10, y + 80, width - 20, 30)
        },
        {
        "name": "tower3",
        "price": 200,
        "button": pygame.Rect(x + 10, y + 120, width - 20, 30)
        },
        {
        "name": "tower4",
        "price": 250,
        "button": pygame.Rect(x + 10, y + 160, width - 20, 30)
        }
    ]

    def draw(self, screen):
        # Teken het menu alleen als het zichtbaar is
        if not self.visible:
            return

        pygame.draw.rect(screen, (50, 70, 50), self.rect)  # achtergrond v menu
        # Teken de rand van het menu
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        # Teken de titel van het menu
        #write("Koop een toren:", (self.rect.x + 10, self.rect.y + 10))
        
        # Teken elke toren-optie knop
        for tower in self.tower_options:
            # Teken de achtergrond van de knop
            pygame.draw.rect(screen, (200, 190, 70), tower["button"])
            # Teken de naam en prijs van de toren
            button_text = f"{tower['name']} - {tower['price']} coins"
            write(button_text, (tower["button"].x + 5, tower["button"].y + 5))
    
    def handle_click(self, mouse_position, player_coins):
        # Doe niets als het menu verborgen is
        if not self.visible:
            return (None, 0)
        
     
        # Controleer of er op een toren-knop is geklikt
        for tower in self.tower_options:
            if tower["button"].collidepoint(mouse_position):
                # Controleer of de speler genoeg munten heeft
                if player_coins >= tower["price"]:
                    print(f"{tower['name']} gekocht!")
                    return (tower["name"], tower["price"])  # Geef de kosten terug om af te trekken
        
        # Geef 0 terug als er geen geldige aankoop is gedaan
        return (None, 0)
   

menu_icon = pygame.image.load("assets/menu_images.png")
menu_icon = pygame.transform.scale(menu_icon, (48, 48))
menu_icon_rect = pygame.Rect(0, 0, 48, 48)

# Maak het menu object aan
game_menu = menu(10, 50, 200, 200)


towers = []
placed_tower_positions = []  # Houdt bij waar torens zijn geplaatst
selected_tower_type = None


# Functie om te controleren of een positie geldig is voor een toren
def is_valid_tower_position(grid_x, grid_y):
    # Check of deze positie niet op het pad ligt
    if (grid_x, grid_y) in path_tiles:
        return False
    
    # Check of er al een toren staat op deze positie
    if (grid_x, grid_y) in placed_tower_positions:
        return False
    
    # Check of het binnen de grenzen van het scherm is
    if grid_x < 0 or grid_x >= WIDTH or grid_y < 0 or grid_y >= HEIGHT:
        return False
    
    return True

# We maken een ghostbeeld voor de toren preview
tower_preview = None
ghost_image = None



# set up gameloop

#al voor een deel herschreven maar naamgeving trekt nog op niks
run = True
while run:
    clock.tick(FPS)
    # event handling (all input goes here)
    def handle_events():
        mouse_x, mouse_y = pygame.mouse.get_pos()  # user input
        global tower_preview, ghost_image
        grid_x, grid_y = get_grid_position(mouse_x, mouse_y) 
        global run, selected_tower_type, tower_preview, ghost_image
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x, grid_y = get_grid_position(mouse_x, mouse_y)
                
                # Check if the menu icon was clicked
                if menu_icon_rect.collidepoint(event.pos):
                    game_menu.visible = not game_menu.visible
                    print("Menu icon clicked")

        if game_menu.visible:
            for option in game_menu.tower_options:
                if option["button"].collidepoint(mouse_x, mouse_y):
                    selected_tower_type = option["name"]
                    print(f"Selected tower type: {selected_tower_type}")
                    break
            # Handle tower placement
            if selected_tower_type and event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse is clicked
                if event.button == 1:  # Left mouse button
                    # Check if the position is valid for placing a tower
                    tower_price = tower_stats[selected_tower_type]["cost"]
                    if coins >= tower_price and is_valid_tower_position(grid_x, grid_y):
                        # Create a new tower and add it to the list
                        tower_image = tower_images[selected_tower_type]
                        ghost_image = tower_image[0]
                        stats = tower_stats[selected_tower_type]
                        tower = Tower(grid_x, grid_y, tower_images[selected_tower_type], stats["range"], stats["damage"])
                        level_manager.towers.append(tower)
                        placed_tower_positions.append((grid_x, grid_y))
                        ghost_image = None
                        selected_tower_type = None
                        coins -= tower_price

    # update game logic (enemies, towers, etc.)
    def update_game(): 
        level_manager.update()
        
        
        for tower in level_manager.towers:
            tower.update(level_manager.enemies)

        for enemy in level_manager.enemies:
            if enemy.reached_goal:
                base.health -= enemy.damage
                level_manager.enemies.remove(enemy)
                if base.health <= 0:
                    print("Game Over")
                    run = False

        if getattr(level_manager, 'game_over', False):
            print("Game Over")
            run = False
        if getattr(level_manager, 'game_won', False):
            print("Game Won")
            run = False
    # render everything (map tower UI enemies etc)
    def render():
        WINDOW.blit(map, (0, 0))
        # Draw the base
        base.draw(WINDOW)
        # Draw the spawn point
        Spawn.draw(WINDOW)
        
        # Draw the towers
        for tower in level_manager.towers:
            tower.draw(WINDOW)
        
        # Draw the enemies
        for enemy in level_manager.enemies:
            enemy.draw(WINDOW)
        
        # Draw the coins
        WINDOW.blit(coin_icon, (10, 10))
        write(f"Coins: {coins}", (40, 10))

        # Draw the menu icon
        WINDOW.blit(menu_icon, (10, 40))
        # Draw the menu
        game_menu.draw(WINDOW)
        # Draw the ghost image if it exists
        if ghost_image:
            ghost_rect = ghost_image.get_rect(topleft=(grid_x, grid_y))
            WINDOW.blit(ghost_image, ghost_rect.topleft)

    current_time = pygame.time.get_ticks()
    if current_time - last_coin_time >= 1000:
        coins += 10
        last_coin_time = current_time
    pygame.display.update()
    # Call the functions
    handle_events()
    update_game()
    render()
pygame.quit()
