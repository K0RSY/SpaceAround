import pygame as pg
from settings import *

class Planet():
    def __init__(self, game, radius, position_x, position_y):
        self.game = game

        self.radius = radius
        
        self.position_x = position_x
        self.position_y = position_y

    def draw(self):
        screen_top = self.game.player.position_y - self.game.player.screen_y
        screen_bottom = self.game.player.position_y + self.game.player.screen_y
        screen_left = self.game.player.position_x - self.game.player.screen_x
        screen_right = self.game.player.position_x + self.game.player.screen_x

        top = self.position_y - self.radius
        bottom = self.position_y + self.radius
        left = self.position_x - self.radius
        right = self.position_x + self.radius

        if top < screen_bottom and bottom > screen_top and left < screen_right and right > screen_left:
            pg.draw.circle(self.game.screen, "white", (self.position_x - self.game.player.position_x + self.game.player.screen_x, self.position_y - self.game.player.position_y + self.game.player.screen_y), self.radius, LINE_WIDTH)