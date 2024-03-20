import pygame
import globals


class WndMain(pygame.sprite.Sprite):
    def __init__(self, wnd_main_width, wnd_main_height):
        super().__init__()
        self.image = pygame.Surface((wnd_main_width, wnd_main_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (globals.WND_ZOOM_IN_WIDTH, 0)
        self.image.fill(globals.MAIN_WND_COLOR)
        self.image.set_alpha(255)  # 0 is fully transparent and 255 fully opaque.

    def update(self):
        self.image.fill(globals.MAIN_WND_COLOR)
