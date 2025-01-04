import pygame as pg
from player import *
from space import *
from planet import *
from gui import *

class Window():
    def __init__(self):
        pg.init()
        pg.display.set_caption("SpaceAround")
        pg.mouse.set_visible(False)

        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.player = Player(self)
        self.space = Space(self)
        self.gui = Gui(self)

        self.planets = []
        self.planets.append(Planet(self, 1000, 2000, 0, None, 0))
        self.planets.append(Planet(self, 100, 750, -1, self.planets[0], 2))
        self.planets.append(Planet(self, 50, 925, -1, self.planets[1], -20))

    def check_quit(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                quit()

    def update(self):
        pg.display.update()
        self.delta_time = self.clock.tick(TPS) / 1000

        self.tick()
        self.draw()
        self.check_quit()

    def tick(self):
        for planet in self.planets:
            planet.tick()

        self.player.tick()

    def draw(self):
        self.space.draw()

        for planet in self.planets:
            planet.draw()

        self.player.draw()
        self.gui.draw()

if __name__ == "__main__":
    window = Window()

    while 1:
        window.update()
