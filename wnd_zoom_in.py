import pygame
import globals


class WndZoomIn(pygame.sprite.Sprite):
    def __init__(self, wnd_zoom_in_width, wnd_zoom_in_height):
        super().__init__()
        self.image = pygame.Surface((wnd_zoom_in_width, wnd_zoom_in_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.image.fill(globals.ZOOM_IN_WND_COLOR)
        self.image.set_alpha(255)  # 0 is fully transparent and 255 fully opaque.

    def update(self):
        self.image.fill(globals.ZOOM_IN_WND_COLOR)
