import pygame as pg
from settings import *
from calc import *
from explotion import *

class Planet():
    def __init__(self, game, position_x, position_y, radius, gravity_radius, sun=False, parent=None, speed=0):
        self.game = game
        self.deleated = False

        self.radius = radius
        self.gravity_radius = gravity_radius
        self.sun = sun

        self.on_screen = False
        self.orbit_on_screen = False
        self.gravity_on_screen = False
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

    def draw_parent_orbit(self):
        if not self.parent is None:
            top = self.parent.position_y - self.distance
            bottom = self.parent.position_y + self.distance
            left = self.parent.position_x - self.distance
            right = self.parent.position_x + self.distance
            if top < self.parent.screen_bottom and bottom > self.screen_top and left < self.screen_right and right > self.screen_left:
                pg.draw.circle(self.game.screen, "grey17", (self.parent.position_x - self.game.player.position_x + self.game.player.screen_x, self.parent.position_y - self.game.player.position_y + self.game.player.screen_y), self.distance, LINE_WIDTH)
                self.orbit_on_screen = True
            else:
                self.orbit_on_screen = False

    def draw_planet(self):
        top = self.position_y - self.radius
        bottom = self.position_y + self.radius
        left = self.position_x - self.radius
        right = self.position_x + self.radius

        if top < self.screen_bottom and bottom > self.screen_top and left < self.screen_right and right > self.screen_left:
            if self.sun:
                pg.draw.circle(self.game.screen, "orange", (self.position_x - self.game.player.position_x + self.game.player.screen_x, self.position_y - self.game.player.position_y + self.game.player.screen_y), self.radius)
            else:
                pg.draw.circle(self.game.screen, "white", (self.position_x - self.game.player.position_x + self.game.player.screen_x, self.position_y - self.game.player.position_y + self.game.player.screen_y), self.radius, LINE_WIDTH)
            self.on_screen = True
        else:
            self.on_screen = False

    def draw_gravity(self):
        top = self.position_y - self.gravity_radius
        bottom = self.position_y + self.gravity_radius
        left = self.position_x - self.gravity_radius
        right = self.position_x + self.gravity_radius

        if top < self.screen_bottom and bottom > self.screen_top and left < self.screen_right and right > self.screen_left:
            pg.draw.circle(self.game.screen, "grey34", (self.position_x - self.game.player.position_x + self.game.player.screen_x, self.position_y - self.game.player.position_y + self.game.player.screen_y), self.gravity_radius, LINE_WIDTH)
            self.gravity_on_screen = True
        else:
            self.gravity_on_screen = False

    def draw(self):
        self.screen_top = self.game.player.position_y - self.game.player.screen_y
        self.screen_bottom = self.game.player.position_y + self.game.player.screen_y
        self.screen_left = self.game.player.position_x - self.game.player.screen_x
        self.screen_right = self.game.player.position_x + self.game.player.screen_x

        self.draw_gravity()
        self.draw_planet()
        self.draw_parent_orbit()
            
    def bounce(self, ratio, relative_player_x, relative_player_y, player_distace_multiplier):
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

        player_speed = self.game.player.speed * ratio

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
                if self.sun:
                    self.game.exit()
                else:
                    if self.game.player.speed >= LETHAL_PLAYER_SPEED_ON_PIXEL_RADIUS * self.radius:
                        self.deleated = True
                        self.game.create_object(Explotion(self.game, self.position_x, self.position_y, self.radius, self.gravity_radius, GRAVITY_MAX_FORCE))
                        self.bounce(BOUNCE_EXPLOTION_RATIO, relative_player_x, relative_player_y, player_distace_multiplier)
                    else:
                        self.bounce(BOUNCE_RATIO, relative_player_x, relative_player_y, player_distace_multiplier)

    def rotate(self):
        if not self.parent is None:
            self.rotation += self.game.delta_time * self.speed

            relative_x = find_a(self.rotation, self.distance)
            relative_y = find_b(self.rotation, self.distance)

            self.position_x = self.parent.position_x + relative_x
            self.position_y = self.parent.position_y + relative_y

    def apply_gravity(self):
        if self.gravity_on_screen == True:
            relative_player_x = self.position_x - self.game.player.position_x
            relative_player_y = self.position_y - self.game.player.position_y

            player_distace = find_c(relative_player_x, relative_player_y)

            if player_distace <= self.gravity_radius:
                gravity_acceleration = GRAVITY_MAX_FORCE * self.game.delta_time * .5 * (1 - player_distace / self.gravity_radius)

                gravity_rotation = find_degree(relative_player_x, relative_player_y)
                gravity_rotation += 180

                gravity_acceleration_x = find_a(gravity_rotation, gravity_acceleration)
                gravity_acceleration_y = find_b(gravity_rotation, gravity_acceleration)
                
                self.game.player.speed_x += gravity_acceleration_x
                self.game.player.speed_y += gravity_acceleration_y

    def tick(self):
        self.rotate()
        self.apply_gravity()
        self.check_collision()