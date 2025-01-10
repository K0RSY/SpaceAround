import pygame as pg
from player import *
from space import *
from planet import *
from gui import *
from explotion import *

class Window():
    def __init__(self):
        pg.init()
        pg.display.set_caption("SpaceAround")
        pg.mouse.set_visible(False)

        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.objects = []

        self.player = Player(self)
        self.space = Space(self)
        self.gui = Gui(self)

        self.objects.append(Planet(self,  1200, 0, 400, 1000))
        self.objects.append(Planet(self, -600, 1, 100, 250, self.objects[0], 2))
        self.objects.append(Planet(self, -150, 1, 50, 150, self.objects[1], -20))

    def check_quit(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                quit()

    def create_object(self, object):
        self.objects.append(object)

    def update(self):
        pg.display.update()
        self.delta_time = self.clock.tick(TPS) / 1000

        self.tick()
        self.draw()
        self.check_quit()

    def tick(self):
        for object in self.objects:
            if not object.deleated:
                object.tick()
            else:
                self.objects.remove(object)

        self.player.tick()

    def draw(self):
        self.space.draw()

        for object in self.objects:
            object.draw()

        self.player.draw()
        self.gui.draw()

if __name__ == "__main__":
    window = Window()

    while 1:
        window.update()
