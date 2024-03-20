import pygame
import globals


class NoiseSrc(pygame.sprite.Sprite):
    def __init__(self, src_rect_width, src_rect_height):
        super().__init__()
        self.image = pygame.Surface((src_rect_width, src_rect_height))
        self.image.set_alpha(150)  # 0 is fully transparent and 255 fully opaque.
        self.rect = self.image.get_rect()
        self.noise_circles = [0]
        self.delay_circles = globals.DELAY_BTW_CIRCLES
        self.draw()

    def update(self):
        if self.delay_circles == 0:
            self.noise_circles.append(self.noise_circles[-1] + 2 * 10)
            if len(self.noise_circles) > 10:
                self.noise_circles = [0]
            self.delay_circles = globals.DELAY_BTW_CIRCLES
        else:
            self.delay_circles -= 1

        self.draw()

    def draw(self):
        self.image.fill(globals.MAIN_WND_COLOR)
        pygame.draw.circle(self.image, globals.GREEN, (self.rect.width / 2, self.rect.height / 2),
                           globals.NOISE_SIZE[0] / 2, width=2)
        pygame.draw.circle(self.image, globals.RED, (self.rect.width / 2, self.rect.height / 2), 3, width=0)
        for radius in self.noise_circles:
            pygame.draw.circle(self.image, globals.LIGHT_GREEN, (self.rect.width / 2, self.rect.height / 2), radius,
                               width=1)
