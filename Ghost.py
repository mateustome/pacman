import pygame
from Direction import Direction
from GhostBehaviour import GhostBehaviour
from MovableObject import MovableObject


def translate_screen_to_maze(in_coords, in_size=32):
    return int(in_coords[0] / in_size), int(in_coords[1] / in_size)


def translate_maze_to_screen(in_coords, in_size=32):
    return in_coords[0] * in_size, in_coords[1] * in_size

class Ghost(MovableObject):
    def __init__(self, in_surface, x, y, in_size: int, in_game_controller, sprite_path="images/ghost_fright.png"):
        super().__init__(in_surface, x, y, in_size)
        self.game_controller = in_game_controller
        self.sprite_normal = pygame.image.load(sprite_path)
        self.sprite_fright = pygame.image.load("images/ghost_fright.png")

    def reached_target(self):
        if (self.x, self.y) == self.next_target:
            self.next_target = self.get_next_location()
        self.current_direction = self.calculate_direction_to_next_target()

    def set_new_path(self, in_path):
        for item in in_path:
            self.location_queue.append(item)
        self.next_target = self.get_next_location()

    def calculate_direction_to_next_target(self) -> Direction:
        if self.next_target is None:
            if self._renderer.get_current_mode() == GhostBehaviour.CHASE and not self._renderer.is_kokoro_active():
                self.request_path_to_player(self)
            else:
                self.game_controller.request_new_random_path(self)
            return Direction.NONE

        diff_x = self.next_target[0] - self.x
        diff_y = self.next_target[1] - self.y
        if diff_x == 0:
            return Direction.DOWN if diff_y > 0 else Direction.UP
        if diff_y == 0:
            return Direction.LEFT if diff_x < 0 else Direction.RIGHT

        if self._renderer.get_current_mode() == GhostBehaviour.CHASE and not self._renderer.is_kokoro_active():
            self.request_path_to_player(self)
        else:
            self.game_controller.request_new_random_path(self)
        return Direction.NONE

    def request_path_to_player(self, in_ghost):
        player_position = translate_screen_to_maze(in_ghost._renderer.get_hero_position())
        current_maze_coord = translate_screen_to_maze(in_ghost.get_position())
        path = self.game_controller.p.get_path(current_maze_coord[1], current_maze_coord[0], player_position[1],
                                               player_position[0])

        new_path = [translate_maze_to_screen(item) for item in path]
        in_ghost.set_new_path(new_path)

    def automatic_move(self, in_direction: Direction):
        if in_direction == Direction.UP:
            self.set_position(self.x, self.y - 1)
        elif in_direction == Direction.DOWN:
            self.set_position(self.x, self.y + 1)
        elif in_direction == Direction.LEFT:
            self.set_position(self.x - 1, self.y)
        elif in_direction == Direction.RIGHT:
            self.set_position(self.x + 1, self.y)
    def draw(self):
        self.image = self.sprite_fright if self._renderer.is_kokoro_active() else self.sprite_normal
        super(Ghost, self).draw()