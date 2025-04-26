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
font=pygame.font.Font(None,20)

def write(text,location,color=(255,255,255)):
    WINDOW.blit(font.render(text,True,color),location)

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

# object enemy
enemy_image = pygame.image.load("Enemy.png")
path = [(0, 32), (736, 32), (736, 256), (96, 256), (96, 512), (960, 512)]
enemy = Enemy(0, 32, enemy_image, health=100, speed=2, path=path, damage=10)

"""class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("tower.png")
        self.rect = self.image.get_rect(topleft=(x, y))

    def attack(self):
        # orient tower towards enemy, check range, and deal damage + animation
        pass

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
""" 

# define level


# define base
class Base:
    def __init__(self, x, y, image, health):
        self.x = x
        self.y = y
        self.image = image
        self.health = health

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


# set up gameloop
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    enemy.move()

    WINDOW.blit(map, (0, 0))   
    enemy.draw(WINDOW)         
    write("Health: " + str(enemy.health), (enemy.x, enemy.y - 20), (255, 0, 0))     # Health bar above enemy for testing
    write("Base health: " + str(base.health), (832, 32), (255, 0, 0))
    base.draw(WINDOW)
    Spawn.draw(WINDOW)

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
