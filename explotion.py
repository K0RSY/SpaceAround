import pygame as pg
from settings import *

class Explotion():
    def __init__(self, game, position_x, position_y, radius, max_radius, speed):
        self.game = game
        self.deleated = False

        self.radius = radius
        self.max_radius = max_radius
        self.speed = speed

        self.position_x = position_x
        self.position_y = position_y

    def draw(self):
        pg.draw.circle(self.game.screen, "orange", (self.position_x - self.game.player.position_x + self.game.player.screen_x, self.position_y - self.game.player.position_y + self.game.player.screen_y), self.radius, LINE_WIDTH)

    def tick(self):
        if self.radius >= self.max_radius:
            self.deleated = True # удалить себя
        else:
            self.radius += self.speed * self.game.delta_time