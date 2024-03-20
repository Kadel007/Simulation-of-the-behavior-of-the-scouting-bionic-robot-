import pygame
import globals


class Traces(pygame.sprite.Sprite):
    def __init__(self, wnd_main_width, wnd_main_height):
        super().__init__()
        self.image = pygame.Surface((wnd_main_width, wnd_main_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.image.fill(globals.MAIN_WND_COLOR)
        self.image.set_alpha(50)  # 0 is fully transparent and 255 fully opaque.

    def update(self):
        self.image.fill(globals.MAIN_WND_COLOR)

    def show_track(self, trace_list):
        for point in trace_list:
            pygame.draw.circle(self.image, globals.MAROON, point, 1, width=0)