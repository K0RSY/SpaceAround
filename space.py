import pygame as pg
from settings import *

class Space():
    def __init__(self, game):
        self.game = game

    def draw(self):
        self.game.screen.fill("black")

        screen_width, screen_height = self.game.screen.get_size()

        ship_offset_x = self.game.player.position_x % STAR_FREQUENCY
        ship_offset_y = self.game.player.position_y % STAR_FREQUENCY

        screen_offset_x = self.game.player.screen_x % STAR_FREQUENCY
        screen_offset_y = self.game.player.screen_y % STAR_FREQUENCY

        stars_offset_x = screen_offset_x - ship_offset_x
        stars_offset_y = screen_offset_y - ship_offset_y

        stars_count_x = screen_width // STAR_FREQUENCY + 2
        stars_count_y = screen_height // STAR_FREQUENCY + 2

        for x in range(stars_count_x):
            for y in range(stars_count_y):
                pg.draw.circle(self.game.screen, "gray", (x * STAR_FREQUENCY + stars_offset_x, y * STAR_FREQUENCY + stars_offset_y), LINE_WIDTH)
