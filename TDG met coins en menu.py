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
enemy = Enemy(0, 32, enemy_image, health=100, speed=2, path=path, damage=10)

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
            return 0
            
        # Controleer of er op een toren-knop is geklikt
        for tower in self.tower_options:
            if tower["button"].collidepoint(mouse_position):
                # Controleer of de speler genoeg munten heeft
                if player_coins >= tower["price"]:
                    print(f"{tower['name']} gekocht!")
                    return tower["price"]  # Geef de kosten terug om af te trekken
        
        # Geef 0 terug als er geen geldige aankoop is gedaan
        return 0
   

menu_icon = pygame.image.load("menu_images.png")
menu_icon = pygame.transform.scale(menu_icon, (48, 48))
menu_icon_rect = pygame.Rect(0,0,48,48 )

# Maak het menu object aan
game_menu = menu(10, 50, 200, 200)

# set up gameloop
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Klik op menu-icoon
            if menu_icon_rect.collidepoint(mouse_pos):
                game_menu.visible = not game_menu.visible  # Toggle menu open/dicht

            # Klik op menu-opties als menu zichtbaar is
            if game_menu.visible:
                cost = game_menu.handle_click(mouse_pos, coins.amount)
                if cost > 0:
                    coins.amount -= cost

    enemy.move()

    WINDOW.blit(map, (0, 0))
    enemy.draw(WINDOW)
    write("Health: " + str(enemy.health), (enemy.x, enemy.y - 20), (255, 0, 0))
    write("Base health: " + str(base.health), (832, 32), (255, 0, 0))
    base.draw(WINDOW)
    Spawn.draw(WINDOW)

    coin_icon_x = WIDTH - 130
    coin_icon_y = 60
    WINDOW.blit(coin_icon, (coin_icon_x, coin_icon_y))
    coins.update()
    write(str(coins.amount), (coin_icon_x + 30, coin_icon_y + 4), (255, 215, 0))

    # Menu-icoon tekenen
    WINDOW.blit(menu_icon, (menu_icon_rect.x, menu_icon_rect.y))

    # Menu tekenen
    game_menu.draw(WINDOW)  # Gebruik het game_menu object

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

    # Update the display
    pygame.display.update()

pygame.quit()
