import pygame

def load_image(path, frames):
    sheet = pygame.image.load(path).convert_alpha()
    frame_width = sheet.get_width() // frames
    frame_height = sheet.get_height()
    return [sheet.subsurface((i * frame_width, 0, frame_width, frame_height)) for i in range(frames)]


tower_images = {
    "tower1": load_image("assets/Armored Skeleton-Attack01.png", 8),
    "tower2": load_image("assets/Archer-Attack01.png", 9),
    "tower3": load_image("assets/Soldier-Attack01.png", 6),
    "tower4": load_image("assets/Wizard-Attack01.png", 6),

}

tower_stats = {
    "tower1": {"range": 100, "damage": 10, "cost": 100},
    "tower2": {"range": 125, "damage": 15, "cost": 150},
    "tower3": {"range": 175, "damage": 20, "cost": 200},
    "tower4": {"range": 200, "damage": 25, "cost": 250},
}

enemy_images = {
    "enemy1": [pygame.image.load("assets/Armored Skeleton-attack01.png").convert_alpha()],
    "enemy2": [pygame.image.load("assets/Archer-Attack01.png").convert_alpha()],
    "enemy3": [pygame.image.load("assets/Soldier-Attack01.png").convert_alpha()],
}

def load_first_frame(path, total_frames):
    sheet = pygame.image.load(path).convert_alpha()
    first_frame = sheet.subsurface((0, 0, 100, 100))
    return [first_frame]



game_map_1 = pygame.image.load("assets/mapTBC.png").convert_alpha()


UI_images = {
    "start_button": pygame.image.load("assets/start_button.png").convert_alpha(),
    "exit_button": pygame.image.load("assets/exit_button.png").convert_alpha(),
    "UI_frame": pygame.image.load("assets/UI_frame.png").convert_alpha(),
    "UI_frame2": pygame.image.load("assets/UI_frame2.png").convert_alpha(),
    "UI_frame3": pygame.image.load("assets/UI_frame3.png").convert_alpha(),
    "UI_frame4": pygame.image.load("assets/UI_frame4.png").convert_alpha(),
    "coin_icon": pygame.image.load("assets/coin_image.jpg").convert_alpha(),
    "mapTBC": pygame.image.load("assets/mapTBC.png").convert_alpha(),

}

level_data = {
    "level1": {
        "towers": [],
        "enemies": {
            "enemy1": {"position": (50, 50), "health": 100, "speed": 2, "damage": 10},
            "enemy2": {"position": (50, 50), "health": 200, "speed": 3, "damage": 10},
        },
        "map": game_map_1,
        "path": [(0, 32), (736, 32), (736, 256), (96, 256), (96, 512), (960, 512)],
       "waves": [
           {"type": "enemy1", "count": 5, "interval": 1000},
           {"type": "enemy2", "count": 3, "interval": 1500},
       ],
    },
    "level2": {
       "towers": [],
       "enemies": {
           "enemy1": {"position": (50, 50), "health": 100, "speed": 2, "damage": 10},
           "enemy2": {"position": (50, 50), "health": 200, "speed": 3, "damage": 10},
       },
       "map": game_map_1,
       "path": [(0, 32), (736, 32), (736, 256), (96, 256), (96, 512), (960, 512)],
       "waves": [
           {"type": "enemy1", "count": 5, "interval": 1000},
           {"type": "enemy2", "count": 3, "interval": 1500},
       ],
    },
}
