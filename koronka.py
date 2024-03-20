import pygame
import globals


class Koronka(pygame.sprite.Sprite):
    def __init__(self, koronka_width, koronka_height):
        super().__init__()
        self.koronka_width = koronka_width
        self.koronka_height = koronka_height
        self.image = pygame.Surface((self.koronka_width, self.koronka_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, globals.WND_ZOOM_IN_HEIGHT)
        self.image.fill(globals.WHITE)
        self.image.set_alpha(255)  # 0 is fully transparent and 255 fully opaque.
        frame_rect = (50, 50, 100, 100)

        sensor_colors = [pygame.Color("red"), pygame.Color("green4"), pygame.Color("blue"),
                         pygame.Color("mediumvioletred")]
        sensor_coords = [(25, 25), (150, 25), (150, 160), (25, 160)]

        pygame.draw.line(self.image, globals.BLACK, (0, 0), (self.koronka_width, 0), 1)  # top divider
        pygame.draw.rect(self.image, pygame.Color("deepskyblue"), frame_rect, width=1)  # corona
        pygame.draw.circle(self.image, sensor_colors[0], (50, 50), 3, width=0)  # sensor 1
        pygame.draw.circle(self.image, sensor_colors[1], (150, 50), 3, width=0)  # sensor 2
        pygame.draw.circle(self.image, sensor_colors[2], (150, 150), 3, width=0)  # sensor 3
        pygame.draw.circle(self.image, sensor_colors[3], (50, 150), 3, width=0)  # sensor 4

        font = pygame.font.SysFont("monospace", 16)

        for i in range(0, 4):
            label = font.render("S" + str(i + 1), True, sensor_colors[i])
            label_rect = label.get_rect()
            label_rect.topleft = sensor_coords[i]
            self.image.blit(label, label_rect)
