import pygame
import math

class Tower:
    def __init__(self, x, y, image, range_radius, damage_per_second):
        self.x = x
        self.y = y
        self.frames = image
        self.range = range_radius
        self.dps = damage_per_second
        self.last_attack_time = pygame.time.get_ticks()
        self.animation_index = 0
        self.animation_speed = 0.2
        self.frame_timer = 0
        self.attacking = False

    def draw(self, surface):
        frame = self.frames[int(self.animation_index)]
        surface.blit(frame, (self.x, self.y))
        pygame.draw.circle(surface, (255, 0, 0), (self.x + 32, self.y + 32), self.range, 1)

    def update(self, enemies):
        self.attacking = False
        current_time = pygame.time.get_ticks()

        for enemy in enemies:
            dist = math.hypot((self.x + 32) - (enemy.x + 32), (self.y + 32) - (enemy.y + 32))
            if dist <= self.range:
                self.attacking = True
                if current_time - self.last_attack_time >= 1000:
                    enemy.health -= self.dps
                    self.last_attack_time = current_time
                    break  # Only hit one enemy per cycle

        # Animate if attacking
        if self.attacking:
            self.frame_timer += self.animation_speed
            if self.frame_timer >= 1:
                self.animation_index = (self.animation_index + 1) % len(self.frames)
                self.frame_timer = 0
        else:
            self.animation_index = 0  # Reset to idle frame when not attacking
    
    
