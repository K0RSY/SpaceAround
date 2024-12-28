import pygame as pg
from math import sin, cos, radians, atan, degrees
from settings import *
from random import randint

class Player():
    def __init__(self, game):
        self.game = game

        self.rotation = 0
        self.rotation_speed = 0

        self.position_x = 0
        self.position_y = 0
        self.speed = 0
        self.speed_x = 0
        self.speed_y = 0

        self.screen_x = 0
        self.screen_y = 0

    def accelerate(self):
        acceleration = PLAYER_ACCELERATION_SPEED * self.game.squared_delta_time
        
        self.speed_x += cos(radians(self.rotation)) * acceleration
        self.speed_y += sin(radians(self.rotation)) * acceleration

    def slow_down(self):
        slowdown = PLAYER_SLOWDOWN_SPEED * self.game.squared_delta_time
        self.speed = (self.speed_x ** 2 + self.speed_y ** 2) ** 0.5

        if self.speed != 0:
            speed_multiplier = (self.speed - slowdown) / self.speed
        else:
            speed_multiplier = 0

        self.speed_x *= speed_multiplier
        self.speed_y *= speed_multiplier

    def limit_speed(self):
        self.speed = (self.speed_x ** 2 + self.speed_y ** 2) ** 0.5
        
        if self.speed != 0:
            speed_multiplier = min(self.max_speed, max(self.speed, 0)) / self.speed
        else:
            speed_multiplier = 0
        
        self.speed_x *= speed_multiplier
        self.speed_y *= speed_multiplier

    def move(self):
        self.max_speed = PLAYER_MAX_SPEED * self.game.delta_time

        if pg.mouse.get_pressed()[0]:
            self.accelerate()
        self.slow_down()

        self.limit_speed()

        self.position_x += self.speed_x
        self.position_y += self.speed_y

    def rotate(self):
        mouse_x = pg.mouse.get_pos()[0]
        mouse_y = pg.mouse.get_pos()[1]

        relative_mouse_x = self.screen_x - mouse_x
        relative_mouse_y = self.screen_y - mouse_y

        if not relative_mouse_x == 0 and not relative_mouse_y == 0:
            self.rotation = degrees(atan(relative_mouse_y / relative_mouse_x))
            if relative_mouse_x >= 0: self.rotation += 180

    def tick(self):
        self.rotate()
        self.move()

    def draw(self):
        if self.game.delta_time != 0:
            flame_multiplier = (FLAME_LENGHT + randint(0, 200) / 100) / self.game.delta_time / 100
        else:
            flame_multiplier = 0

        half_screen_width = self.game.screen.get_size()[0] // 2
        half_screen_height = self.game.screen.get_size()[1] // 2

        self.screen_x = half_screen_width
        self.screen_y = half_screen_height

        flame_start_x = self.screen_x
        flame_start_y = self.screen_y

        flame_end_x = self.screen_x - cos(radians(self.rotation)) * self.speed * flame_multiplier
        flame_end_y = self.screen_y - sin(radians(self.rotation)) * self.speed * flame_multiplier

        wing_left_x = self.screen_x - cos(radians(self.rotation-SHIP_WING_DEGREE)) * SHIP_LENGHT
        wing_left_y = self.screen_y - sin(radians(self.rotation-SHIP_WING_DEGREE)) * SHIP_LENGHT
        wing_right_x = self.screen_x - cos(radians(self.rotation+SHIP_WING_DEGREE)) * SHIP_LENGHT
        wing_right_y = self.screen_y - sin(radians(self.rotation+SHIP_WING_DEGREE)) * SHIP_LENGHT

        pg.draw.line(self.game.screen, "orange", (flame_start_x, flame_start_y), (flame_end_x, flame_end_y), LINE_WIDTH)
        pg.draw.polygon(self.game.screen, "white", ((flame_start_x, flame_start_y), (wing_left_x, wing_left_y), (wing_right_x, wing_right_y)))