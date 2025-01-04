import pygame as pg
from settings import *
from calc import *

class Planet():
    def __init__(self, game, radius, position_x, position_y, parent, speed):
        self.game = game

        self.radius = radius

        self.on_screen = False
        self.position_x = position_x
        self.position_y = position_y

        self.parent = parent
        self.speed = speed
        if not self.parent is None:
            self.find_rotation()
            self.find_distance()

    def find_rotation(self):
        relative_x = self.parent.position_x - self.position_x
        relative_y = self.parent.position_y - self.position_y

        self.rotation = find_degree(relative_x, relative_y)
        
    def find_distance(self):
        relative_x = self.parent.position_x - self.position_x
        relative_y = self.parent.position_y - self.position_y

        self.distance = find_c(relative_x, relative_y)

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
            
    def bounce(self, relative_player_x, relative_player_y, player_distace_multiplier):
        player_rotation = find_degree(self.game.player.speed_x, self.game.player.speed_y)
        player_rotation += 180

        player_position_x = relative_player_x * player_distace_multiplier
        player_position_y = relative_player_y * player_distace_multiplier

        bounce_rotation = find_degree(player_position_x, player_position_y)

        player_rotation -= bounce_rotation

        if player_rotation > 0:
            player_rotation = (180 - abs(player_rotation))
        else:
            player_rotation = -(180 - abs(player_rotation))

        player_rotation += bounce_rotation

        player_speed = self.game.player.speed * BOUNCE_RATIO

        player_position_x = self.position_x - player_position_x
        player_position_y = self.position_y - player_position_y

        self.game.player.speed_x = find_a(player_rotation, player_speed)
        self.game.player.speed_y = find_b(player_rotation, player_speed)

        self.game.player.position_x = player_position_x
        self.game.player.position_y = player_position_y

    def check_collision(self):
        if self.on_screen == True:
            relative_player_x = self.position_x - self.game.player.position_x
            relative_player_y = self.position_y - self.game.player.position_y

            player_distace = find_c(relative_player_x, relative_player_y)

            player_distace_multiplier = (self.radius + BOUNCE_OFFSET) / player_distace

            if player_distace <= self.radius:
                self.bounce(relative_player_x, relative_player_y, player_distace_multiplier)

    def rotate(self):
        if not self.parent is None:
            self.rotation += self.game.delta_time * self.speed

            relative_x = find_a(self.rotation, self.distance)
            relative_y = find_b(self.rotation, self.distance)

            self.position_x = self.parent.position_x + relative_x
            self.position_y = self.parent.position_y + relative_y

            print(self.rotation, self.position_x, self.position_y)
            print(relative_x, relative_y)

    def tick(self):
        self.rotate()
        self.check_collision()