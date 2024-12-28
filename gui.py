import pygame as pg
from settings import *

class Gui():
    def __init__(self, game):
        self.game = game

    def draw_text(self, text):
        text = text.split("\n")
        for line in range(len(text)):
            font = pg.font.Font(size=20).render(text[line], True, "white")
            offset = (font.get_height() + 10) * line

            text_rect = font.get_rect()
            text_rect.topleft = (0, offset)
            
            self.game.screen.blit(font, text_rect)

    def draw_cursor(self):
        if PLAYER_MAX_SPEED != 0:
            radius = CURSOR_RADIUS * (1 - (self.game.player.speed / PLAYER_MAX_SPEED) / 2)
        else:
            radius = 0
        
        pg.draw.line(self.game.screen, "orange", (pg.mouse.get_pos()[0] + CURSOR_RADIUS, pg.mouse.get_pos()[1]), (pg.mouse.get_pos()[0] - CURSOR_RADIUS, pg.mouse.get_pos()[1]), LINE_WIDTH)
        pg.draw.line(self.game.screen, "orange", (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1] + CURSOR_RADIUS), (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1] - CURSOR_RADIUS), LINE_WIDTH)
        pg.draw.circle(self.game.screen, "orange", pg.mouse.get_pos(), radius, LINE_WIDTH)

    def draw(self):
        self.draw_cursor()

        text = f'TPS: {self.game.clock.get_fps(): .0f}\
                 X: {self.game.player.position_x: .0f} Y: {self.game.player.position_y: .0f}\
                 ROTATION: {self.game.player.rotation: .0f} \
                 SPEED: {self.game.player.speed: .2f}'.replace("                 ", "\n")
        self.draw_text(text)
        
