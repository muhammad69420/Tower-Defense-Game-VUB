import pygame

pygame.init()

print("Starting game")


# Set up the display
WIDTH, HEIGHT = 960, 640
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")


# clock
clock = pygame.time.Clock()
FPS = 40

# set up image
TILE_SIZE = 64
map = pygame.image.load("mapTBC.png")


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
        
        pass

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
""" 

# define base
class Base:
    def __init__(self, x, y, image, health):
        self.x = x
        self.y = y
        self.image = image
        self.health = health

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


"""base_image = pygame.image.load("base.png")
base = Base(832, 512, base_image, health=100)

def base_damage():
    if base.health <= 0:
        print("Game Over")
        pygame.quit()
        exit()
"""
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
    write("Health: " + str(enemy.health), (enemy.x, enemy.y - 20), (255, 0, 0))
    write("Base health: " + str(100), (832, 32), (255, 0, 0))

    # Update the display
    pygame.display.update()

pygame.quit()