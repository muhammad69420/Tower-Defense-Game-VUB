import pygame
import math

pygame.init()

print("Starting game")

# Set up the display
WIDTH, HEIGHT = 960, 640
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# clock
clock = pygame.time.Clock()
FPS = 180  #reduce FPS to 40 for gameplay, 180 for testing

# set up image
TILE_SIZE = 64
map = pygame.image.load("mapTBC.png")

Reached = False

global font
font = pygame.font.Font(None, 20)

def write(text, location, color=(255, 255, 255)):
    WINDOW.blit(font.render(text, True, color), location)

# Functie om muispositie naar grid te converteren
def get_grid_position(mouse_x, mouse_y):
    grid_x = (mouse_x // TILE_SIZE) * TILE_SIZE
    grid_y = (mouse_y // TILE_SIZE) * TILE_SIZE
    return (grid_x, grid_y)

# set up classes
class Enemy:
    def __init__(self, x, y, image, health, speed, path, damage):
        self.x = x
        self.y = y
        self.image = image
        self.path = path
        self.path_index = 0
        self.health = health
        self.speed = speed
        self.damage = damage
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        if self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]

            dx = target_x - self.x
            dy = target_y - self.y
            dist = (dx**2 + dy**2) ** 0.5

            if dist < self.speed:
                self.x, self.y = target_x, target_y
                self.path_index += 1
            else:
                self.x += self.speed * dx / dist
                self.y += self.speed * dy / dist

            self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def damage(self, amount):
        pass
# object enemy
enemy_image = pygame.image.load("Enemy.png")
path = [(0, 32), (736, 32), (736, 256), (96, 256), (96, 512), (960, 512)]
enemy = Enemy(0, 32, enemy_image, health=100, speed=0.3, path=path, damage=10)

class Bases:
    def __init__(self, x, y, image, health):
        self.x = x
        self.y = y
        self.image = image
        self.health = health

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

base_image = pygame.image.load("base1.png")
base = Bases(832, 480, base_image, health=10)
baseCoordinatesX = 896
baseCoordinatesY = 512

base_enemy = pygame.image.load("EnemySpawn.png")
Spawn = Bases(0, 0, base_enemy, health=100000)

# Dit zijn de paden waar de vijand loopt - op deze tiles kan geen toren worden geplaatst
path_tiles = []
for x, y in path:
    # Voeg alle tiles die het pad vormen toe
    grid_x = (x // TILE_SIZE) * TILE_SIZE
    grid_y = (y // TILE_SIZE) * TILE_SIZE
    path_tiles.append((grid_x, grid_y))
    
# Voeg extra paden toe voor het complete pad
# We voegen horizontale en verticale secties toe tussen de punten
for i in range(len(path) - 1):
    x1, y1 = path[i]
    x2, y2 = path[i + 1]
    
    # Als horizontale beweging
    if y1 == y2:
        step = 1 if x2 > x1 else -1
        for x in range(x1, x2, step * TILE_SIZE):
            grid_x = (x // TILE_SIZE) * TILE_SIZE
            grid_y = (y1 // TILE_SIZE) * TILE_SIZE
            if (grid_x, grid_y) not in path_tiles:
                path_tiles.append((grid_x, grid_y))
    
    # Als verticale beweging
    if x1 == x2:
        step = 1 if y2 > y1 else -1
        for y in range(y1, y2, step * TILE_SIZE):
            grid_x = (x1 // TILE_SIZE) * TILE_SIZE
            grid_y = (y // TILE_SIZE) * TILE_SIZE
            if (grid_x, grid_y) not in path_tiles:
                path_tiles.append((grid_x, grid_y))


class coins:
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
coin_icon = pygame.image.load("coin_image.png")
coin_icon = pygame.transform.scale(coin_icon, (24, 24))

class menu:  
    def __init__(self, x, y, width, height):
        # de rechthoek van het menu
        self.rect = pygame.Rect(x, y, width, height)
        # Menu begint verborgen
        self.visible = False
        
        # Stel de toren-opties in met hun posities en kosten
        self.tower_options = [
            {
                "name": "kanon", 
                "price": 100,
                "button": pygame.Rect(x + 10, y + 40, width - 20, 30)
            },
            {
                "name": "Boogschutterstoren", 
                "price": 150,
                "button": pygame.Rect(x, y + 80, width, 30)
            },
            {
                "name": "Wizard toren", 
                "price": 200,
                "button": pygame.Rect(x + 10, y + 120, width - 20, 30)
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
   

menu_icon = pygame.image.load("menu_images.png")
menu_icon = pygame.transform.scale(menu_icon, (48, 48))
menu_icon_rect = pygame.Rect(0, 0, 48, 48)

# Maak het menu object aan
game_menu = menu(10, 50, 200, 200)

class Tower:
    def __init__(self, x, y, image, range_radius, damage_per_second):
        self.x = x
        self.y = y
        self.image = image
        self.range = range_radius
        self.dps = damage_per_second
        self.last_attack_time = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        # Optioneel: range cirkel tekenen
        pygame.draw.circle(surface, (255, 0, 0), (self.x + 32, self.y + 32), self.range, 1)

    def attack(self, enemies):
        current_time = pygame.time.get_ticks()
        for enemy in enemies:
            distance = math.hypot((self.x + 32) - (enemy.x + 32), (self.y + 32) - (enemy.y + 32))
            if distance <= self.range:
                if current_time - self.last_attack_time >= 1000:  # elke seconde
                    enemy.health -= self.dps
                    print(f"Enemy hit! Health: {enemy.health}")
                    self.last_attack_time = current_time

towers = []
placed_tower_positions = []  # Houdt bij waar torens zijn geplaatst
selected_tower_type = None
tower_kanon_image = pygame.image.load("kanon.png")
tower_boog_image = pygame.image.load("boogschutters_toren.png")
tower_wizard_image = pygame.image.load("wizard_toren.png")

tower_kanon_image = pygame.transform.scale(tower_kanon_image, (64, 64))
tower_boog_image = pygame.transform.scale(tower_boog_image, (64, 64))
tower_wizard_image = pygame.transform.scale(tower_wizard_image, (64, 64))

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
run = True
while run:
    clock.tick(FPS)
    
    # Voor preview van de toren-plaatsing
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x, grid_y = get_grid_position(mouse_x, mouse_y)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Positie van de muisklik

            # Klik op menu-icoon
            if menu_icon_rect.collidepoint(mouse_pos):
                game_menu.visible = not game_menu.visible  # Zet het menu zichtbaar of onzichtbaar

            # Klik op menu-opties als menu zichtbaar is
            elif game_menu.visible:
                selected_tower_type, cost = game_menu.handle_click(mouse_pos, coins.amount)
                if cost > 0:  # Als toren is gekocht, trek munten af
                    coins.amount -= cost
                    
                    # Stel het juiste ghost-image in voor de preview
                    if selected_tower_type == "kanon":
                        ghost_image = tower_kanon_image.copy()
                        ghost_image.set_alpha(150)  # Maak het half-transparant
                    elif selected_tower_type == "Boogschutterstoren":
                        ghost_image = tower_boog_image.copy()
                        ghost_image.set_alpha(150)
                    elif selected_tower_type == "Wizard toren":
                        ghost_image = tower_wizard_image.copy()
                        ghost_image.set_alpha(150)

            # Klik op de map om toren te plaatsen als er een toren geselecteerd is
            elif selected_tower_type:
                # Bepaal de gridpositie
                grid_x, grid_y = get_grid_position(mouse_pos[0], mouse_pos[1])
                
                # Controleer of deze positie geldig is
                if is_valid_tower_position(grid_x, grid_y):
                    # Plaatsen van de toren op de gridpositie
                    if selected_tower_type == "kanon":
                        towers.append(Tower(grid_x, grid_y, tower_kanon_image, range_radius=100, damage_per_second=20))
                        placed_tower_positions.append((grid_x, grid_y))
                        
                    elif selected_tower_type == "Boogschutterstoren":
                        towers.append(Tower(grid_x, grid_y, tower_boog_image, range_radius=120, damage_per_second=15))
                        placed_tower_positions.append((grid_x, grid_y))
                        
                    elif selected_tower_type == "Wizard toren":
                        towers.append(Tower(grid_x, grid_y, tower_wizard_image, range_radius=140, damage_per_second=10))
                        placed_tower_positions.append((grid_x, grid_y))
                        

                    selected_tower_type = None  # Reset de geselecteerde toren na plaatsen
                    ghost_image = None  # Verwijder preview
                else:
                    print("Ongeldige positie voor toren!")

    enemy.move()

    WINDOW.blit(map, (0, 0))
    
    def draw_grid():
    # Grote gridlijnen
        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(WINDOW, (150, 150, 150), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(WINDOW, (150, 150, 150), (0, y), (WIDTH, y))

    # Subgrids van 16 pixels
    sub_tile_size = 16
    for x in range(0, WIDTH, sub_tile_size):
        pygame.draw.line(WINDOW, (200, 200, 200), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, sub_tile_size):
        pygame.draw.line(WINDOW, (200, 200, 200), (0, y), (WIDTH, y), 1)

    
    # Teken een duidelijke highlight voor de huidige muispositie als er een toren geselecteerd is
    if selected_tower_type and ghost_image:
        if is_valid_tower_position(grid_x, grid_y):
            # Groene highlight voor geldige posities
            pygame.draw.rect(WINDOW, (0, 255, 0, 100), (grid_x, grid_y, TILE_SIZE, TILE_SIZE), 2)
            # Toon de preview van de toren
            WINDOW.blit(ghost_image, (grid_x, grid_y))
        else:
            # Rode highlight voor ongeldige posities
            pygame.draw.rect(WINDOW, (255, 0, 0, 100), (grid_x, grid_y, TILE_SIZE, TILE_SIZE), 2)
    
    enemy.draw(WINDOW)
    write("Health: " + str(enemy.health), (enemy.x, enemy.y - 20), (255, 0, 0))
    write("Base health: " + str(base.health), (832, 32), (255, 0, 0))
    base.draw(WINDOW)
    Spawn.draw(WINDOW)

    # Teken alle torens
    for tower in towers:
        tower.draw(WINDOW)
        tower.attack([enemy])  # laat toren vijand aanvallen als binnen bereik

    coin_icon_x = WIDTH - 130
    coin_icon_y = 60
    WINDOW.blit(coin_icon, (coin_icon_x, coin_icon_y))
    coins.update()
    write(str(coins.amount), (coin_icon_x + 30, coin_icon_y + 4), (255, 215, 0))

    # Menu-icoon tekenen
    WINDOW.blit(menu_icon, (menu_icon_rect.x, menu_icon_rect.y))

    # Menu tekenen
    game_menu.draw(WINDOW)

    distance = math.hypot(enemy.x - baseCoordinatesX, enemy.y - baseCoordinatesY)

    if distance < 5 and not Reached:
        base.health -= enemy.damage
        print(f"Reached target! Health now: {base.health}")
        Reached = True  # Prevent repeating

    if base.health <= 0:
        write("Game Over", (WIDTH // 2 - 50, HEIGHT // 2), (255, 0, 0))
        base.health = 0
        pygame.display.update()
        pygame.time.delay(10000)
        pygame.quit()
        exit()

    draw_grid()
    pygame.display.update()

pygame.quit()
