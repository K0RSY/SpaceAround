import pygame as pg
from settings import *
from random import randint
from calc import *

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
        acceleration = PLAYER_ACCELERATION_SPEED * self.game.delta_time * .5

        acceleration_x = find_a(self.rotation, acceleration)
        acceleration_y = find_b(self.rotation, acceleration)
        
        self.speed_x += acceleration_x
        self.speed_y += acceleration_y
    
    def slow_down(self):
        slowdown = PLAYER_SLOWDOWN_SPEED * self.game.delta_time * .5
        speed = find_c(self.speed_x, self.speed_y)

        if speed != 0:
            speed_multiplier = (speed - slowdown) / speed
        else:
            speed_multiplier = 0

        self.speed_x *= speed_multiplier
        self.speed_y *= speed_multiplier

    def limit_speed(self):
        speed = find_c(self.speed_x, self.speed_y)
        
        if speed > 0:
            speed_multiplier = min(PLAYER_MAX_SPEED, max(speed, 0)) / speed
        else:
            speed_multiplier = 0
        
        self.speed_x *= speed_multiplier
        self.speed_y *= speed_multiplier

    def calculate_speed(self):
        self.speed = find_c(self.speed_x, self.speed_y)

    def calculate_half_speed(self):
        if pg.mouse.get_pressed()[0]:
            self.accelerate()
        self.slow_down()

        self.limit_speed()

    def move(self):
        self.calculate_half_speed()

        self.position_x += self.speed_x * self.game.delta_time
        self.position_y += self.speed_y * self.game.delta_time

        self.calculate_half_speed()

        self.calculate_speed()

    def rotate(self):
        mouse_x = pg.mouse.get_pos()[0]
        mouse_y = pg.mouse.get_pos()[1]

        relative_mouse_x = self.screen_x - mouse_x
        relative_mouse_y = self.screen_y - mouse_y

        self.rotation = find_degree(relative_mouse_x, relative_mouse_y, self.rotation)

    def tick(self):
        self.rotate()
        self.move()

    def draw(self):
        flame_multiplier = (FLAME_LENGHT + randint(-FLAME_MAX_OFFSET, FLAME_MAX_OFFSET)) * (self.game.player.speed / PLAYER_MAX_SPEED) + SHIP_LENGHT
        
        half_screen_width = self.game.screen.get_size()[0] // 2
        half_screen_height = self.game.screen.get_size()[1] // 2

        self.screen_x = half_screen_width
        self.screen_y = half_screen_height

        flame_start_x = self.screen_x
        flame_start_y = self.screen_y

        flame_end_x = self.screen_x - find_a(self.rotation, flame_multiplier)
        flame_end_y = self.screen_y - find_b(self.rotation, flame_multiplier)

        wing_left_x = self.screen_x - find_a(self.rotation - SHIP_WING_DEGREE, SHIP_LENGHT)
        wing_left_y = self.screen_y - find_b(self.rotation - SHIP_WING_DEGREE, SHIP_LENGHT)
        wing_right_x = self.screen_x - find_a(self.rotation + SHIP_WING_DEGREE, SHIP_LENGHT)
        wing_right_y = self.screen_y - find_b(self.rotation + SHIP_WING_DEGREE, SHIP_LENGHT)

        pg.draw.line(self.game.screen, "orange", (flame_start_x, flame_start_y), (flame_end_x, flame_end_y), LINE_WIDTH)
        pg.draw.polygon(self.game.screen, "white", ((flame_start_x, flame_start_y), (wing_left_x, wing_left_y), (wing_right_x, wing_right_y)))