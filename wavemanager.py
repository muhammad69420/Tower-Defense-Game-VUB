import pygame

class LevelManager:
    def __init__(self, level_data):
        self.level_data = level_data
        self.current_level = "level1"
        self.towers = []
        self.enemies = []
        self.map = self.level_data[self.current_level]['map']
        self.path = self.level_data[self.current_level]['path']
        self.wave = self.level_data[self.current_level]['waves']
        self.wave_index = 0
        self.pending_spawns = []
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_interval = 1000  # milliseconds
        self.pending_spawns = []

        if self.wave:
            wave_info = self.wave[self.wave_index]
            self.pending_spawns = [(wave_info['type'], wave_info['count'])]
            self.spawn_interval = wave_info['interval']


    def load_level(self):
        # Load the current level data
        level = self.level_data[self.current_level]
        self.towers = level['towers']
        self.enemies = level['enemies']
        self.map = level['map']
        
    def draw(self, surface):
        # Draw the map
        surface.blit(self.map, (0, 0))

        # Draw towers
        for tower in self.towers:
            tower.draw(surface)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(surface)

        # Draw game over or win screen if applicable
        if self.game_over:
            # Draw game over screen
            pass
        elif self.game_won:
            # Draw win screen
            pass

    
    def spawn_enemy(self, enemy_type):
        # Spawn an enemy of the given type
        enemy_data = self.level_data[self.current_level]['enemies'][enemy_type]
        x, y = enemy_data['position']
        health = enemy_data['health']
        speed = enemy_data['speed']
        path = self.level_data[self.current_level]['path']
        damage = enemy_data['damage']
        
        from assets import enemy_images
        from enemy import Enemy
        return Enemy(x, y, enemy_images[enemy_type], health, speed, path, damage)

    def update(self):
        # Spawn enemies based on timer
        current_time = pygame.time.get_ticks()
        if self.pending_spawns and current_time - self.spawn_timer >= self.spawn_interval:
            enemy_type, count = self.pending_spawns[0]

        if current_time - self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = current_time
            self.enemies.append(self.spawn_enemy(enemy_type))

            if count > 1:
                self.pending_spawns[0] = (enemy_type, count - 1)
            else:
                self.pending_spawns.pop(0)

        #update all enemies
        for enemy in self.enemies:
            enemy.update()
            if not enemy.is_alive():
                self.enemies.remove(enemy)

        #update towers
        for tower in self.towers:
            tower.update(self.enemies)

        # Check for game over or win conditions
        if not self.enemies and not self.pending_spawns:
            if self.wave_index + 1 < len(self.wave):
                self.wave_index += 1
                next_wave = self.wave[self.wave_index]
                self.pending_spawns = [(next_wave['type'], next_wave['count'])]
                self.spawn_interval = next_wave['interval']
            else:
                self.game_won = True
