import pygame as pg
from settings import *
from math import atan, degrees, sin, cos, radians

class Planet():
    def __init__(self, game, radius, position_x, position_y):
        self.game = game

        self.radius = radius

        self.on_screen = False
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
            self.on_screen = True
        else:
            self.on_screen = False

    def tick(self):
        if self.on_screen == True:
            relative_player_x = self.position_x - self.game.player.position_x
            relative_player_y = self.position_y - self.game.player.position_y

            player_distace = (relative_player_x ** 2 + relative_player_y ** 2) ** 0.5

            player_distace_multiplier = (self.radius + BOUNCE_OFFSET) / player_distace

            if player_distace <= self.radius:
                if not self.game.player.speed_x == 0 and not self.game.player.speed_y == 0:
                    player_rotation = degrees(atan(self.game.player.speed_y / self.game.player.speed_x))
                    if self.game.player.speed_x <= 0: player_rotation -= 180
                else:
                    player_rotation = 0

                player_position_x = relative_player_x * player_distace_multiplier
                player_position_y = relative_player_y * player_distace_multiplier

                if not player_position_x == 0 and not player_position_y == 0:
                    bounce_rotation = degrees(atan(player_position_y / player_position_x))
                    if player_position_x >= 0: bounce_rotation == 180
                else:
                    bounce_rotation = 0

                player_rotation -= bounce_rotation

                if player_rotation > 0:
                    player_rotation = (180 - abs(player_rotation))
                else:
                    player_rotation = -(180 - abs(player_rotation))

                player_rotation += bounce_rotation

                player_speed = self.game.player.speed * BOUNCE_RATIO

                player_position_x = self.position_x - player_position_x
                player_position_y = self.position_y - player_position_y

                self.game.player.speed_x = cos(radians(player_rotation)) * player_speed
                self.game.player.speed_y = sin(radians(player_rotation)) * player_speed

                self.game.player.position_x = player_position_x
                self.game.player.position_y = player_position_y