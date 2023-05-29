import pygame
import numpy as np
import tcod
import random
from enum import Enum
from Cookie import Cookie
from Direction import Direction
from GameObject import GameObject
from GameRenderer import GameRenderer

from Ghost import Ghost
from GhostBehaviour import GhostBehaviour
from Hero import Hero
from Menu import menu_selection
from MovableObject import MovableObject
from PacmanGameController import PacmanGameController, translate_maze_to_screen
from Powerup import Powerup
from ScoreType import ScoreType
from Wall import Wall

MAPS = {
    "Iniciar jogo": "./maps/little_map.txt", 
    "Mapa grande": "./maps/big_map.txt",
    "Mapa mini": "./maps/mini_map.txt",
    "Mapa medio": "./maps/little_map.txt", 
}


def run(map_name):
    if(map_name == None):
        map_url = MAPS[menu_selection()];
    else:
        map_url = MAPS[map_name];
    unified_size = 32
    pacman_game = PacmanGameController(map_url)
    size = pacman_game.size
    game_renderer = GameRenderer(size[0] * unified_size, size[1] * unified_size)

    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                game_renderer.add_wall(Wall(game_renderer, x, y, unified_size))

    for cookie_space in pacman_game.cookie_spaces:
        translated = translate_maze_to_screen(cookie_space)
        cookie = Cookie(game_renderer, translated[0] + unified_size / 2, translated[1] + unified_size / 2)
        game_renderer.add_cookie(cookie)

    for powerup_space in pacman_game.powerup_spaces:
        translated = translate_maze_to_screen(powerup_space)
        powerup = Powerup(game_renderer, translated[0] + unified_size / 2, translated[1] + unified_size / 2)
        game_renderer.add_powerup(powerup)

    for i, ghost_spawn in enumerate(pacman_game.ghost_spawns):
        translated = translate_maze_to_screen(ghost_spawn)
        ghost = Ghost(game_renderer, translated[0], translated[1], unified_size, pacman_game,
                      pacman_game.ghost_colors[i % 4])
        game_renderer.add_ghost(ghost)

    pacman = Hero(game_renderer, unified_size, unified_size, unified_size)
    game_renderer.add_hero(pacman)
    game_renderer.set_current_mode(GhostBehaviour.CHASE)
    if(game_renderer.tick(120) == True):
        run('Mapa grande');
    
if __name__ == "__main__":
    run(None);