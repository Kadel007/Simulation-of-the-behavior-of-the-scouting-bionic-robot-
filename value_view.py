import pygame
import globals


class ValueView(pygame.sprite.Sprite):
    def __init__(self, view_width, view_height):
        super().__init__()
        self.view_width = view_width
        self.view_height = view_height
        self.image = pygame.Surface((self.view_width, self.view_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, globals.WND_ZOOM_IN_HEIGHT + globals.KORONKA_HEIGHT)
        self.image.fill(globals.WHITE)
        self.image.set_alpha(255)  # 0 is fully transparent and 255 fully opaque.
        self.start_x = 5
        self.start_y = 10
        self.distance_const = 25
        self.sensor_colors = [pygame.Color("red"), pygame.Color("green4"), pygame.Color("blue"),
                              pygame.Color("mediumvioletred")]
        self.sensor_coords = [(self.start_x, self.start_y + self.distance_const),
                              (self.start_x, self.start_y + self.distance_const * 2),
                              (self.start_x, self.start_y + self.distance_const * 3),
                              (self.start_x, self.start_y + self.distance_const * 4)]
        self.font = pygame.font.SysFont("monospace", 16)
        self.first_in = False

    def update(self, intensity_on_sensor, given_speed_kmh, range_meter, count_time, is_attractive, hear_noise,
               prt_status, min_sensitivity):
        self.image.fill(globals.WHITE)
        pygame.draw.line(self.image, globals.BLACK, (0, 0), (self.view_width, 0), 1)  # top divider

        label = self.font.render("Range(m)= " + f"{float(range_meter):.5}", True, globals.BLACK)
        label_rect = label.get_rect()
        label_rect.topleft = (self.start_x, self.start_y)
        self.image.blit(label, label_rect)

        for i in range(0, 4):
            out_val = f"{float(intensity_on_sensor[i]):.5}"
            label = self.font.render("S" + str(i + 1) + "=" + out_val, True, self.sensor_colors[i])
            label_rect = label.get_rect()
            label_rect.topleft = self.sensor_coords[i]
            self.image.blit(label, label_rect)

        label = self.font.render("Min sens: " + str(min_sensitivity), True, globals.BLACK)
        label_rect = label.get_rect()
        label_rect.topleft = (self.start_x, self.start_y + self.distance_const * 5)
        self.image.blit(label, label_rect)

        label = self.font.render("Speed(m/s) = " + f"{float(given_speed_kmh * 1000 / 3600):.3}", True, globals.BLACK)
        label_rect = label.get_rect()
        label_rect.topleft = (self.start_x, self.start_y + self.distance_const * 6)
        self.image.blit(label, label_rect)

        label = self.font.render("Speed(km/h) = " + f"{float(given_speed_kmh):.3}", True, globals.BLACK)
        label_rect = label.get_rect()
        label_rect.topleft = (self.start_x, self.start_y + self.distance_const * 7)
        self.image.blit(label, label_rect)

        label = self.font.render("Time(s): " + str(int(count_time)), True, globals.BLACK)
        label_rect = label.get_rect()
        label_rect.topleft = (self.start_x, self.start_y + self.distance_const * 8)
        self.image.blit(label, label_rect)

        if hear_noise or self.first_in:
            self.first_in = True
            if is_attractive:
                label = self.font.render("Type: attractive", True, globals.BLUE)
            else:
                label = self.font.render("Type: repulsive", True, globals.RED)
            label_rect = label.get_rect()
            label_rect.topleft = (self.start_x, self.start_y + self.distance_const * 9)
            self.image.blit(label, label_rect)

        if len(prt_status) > 0:
            label = self.font.render(str(prt_status), True, globals.GREEN)
            label_rect = label.get_rect()
            label_rect.topleft = (self.start_x, self.start_y + self.distance_const * 10)
            self.image.blit(label, label_rect)
