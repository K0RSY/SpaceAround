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
        self.planet = Planet(self, 2000, 2000, 0)
        self.gui = Gui(self)

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
        self.planet.tick()
        self.player.tick()

    def draw(self):
        self.space.draw()
        self.planet.draw()
        self.player.draw()
        self.gui.draw()

if __name__ == "__main__":
    window = Window()

    while 1:
        window.update()
