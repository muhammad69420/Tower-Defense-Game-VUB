import pygame
import math

class Enemy:
    def __init__(self, x, y, frames, health, speed, path, damage):
        self.x = x
        self.y = y
        self.frames = frames  # walk animation frames
        self.animation_index = 0
        self.animation_speed = 0.2
        self.frame_timer = 0

        self.path = path
        self.path_index = 0
        self.health = health
        self.speed = speed
        self.damage = damage

        self.reached_goal = False
        self.rect = self.frames[0].get_rect(topleft=(x, y))

    def move(self):
        if self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]

            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.hypot(dx, dy)

            if dist < self.speed:
                self.x, self.y = target_x, target_y
                self.path_index += 1
            else:
                self.x += self.speed * dx / dist
                self.y += self.speed * dy / dist

            self.rect.topleft = (self.x, self.y)
        else:
            self.reached_goal = True

    def update_animation(self):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.animation_index = (self.animation_index + 1) % len(self.frames)
            self.frame_timer = 0

    
    def update(self):
        self.move()
        self.update_animation()


    def draw(self, surface):
        self.update_animation()
        current_frame = self.frames[int(self.animation_index)]
        surface.blit(current_frame, (self.x, self.y))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()
    
    def is_alive(self):
        return self.health > 0

    def die(self):
        #remove enemy from game
        
        pass
