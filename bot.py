import pygame
import globals


class Bot(pygame.sprite.Sprite):
    def __init__(self, bot_width, bot_height):
        super().__init__()
        self.image = pygame.Surface((bot_width, bot_height))
        self.image.fill(globals.ZOOM_IN_WND_COLOR)
        self.rect = self.image.get_rect()

        self.bot_width = bot_width
        self.bot_height = bot_height

        self.is_clicked = False

        ######################################################################
        # put in center image from walk.png sprite sheet
        ######################################################################
        self.animaList = []
        self.anima_pos = 0  # MAX = 7 -number of images in walk.png
        self.anima_delay = globals.BOT_ANIMA_DELAY

        sprt_map = pygame.image.load("walk.png").convert_alpha()
        img_width = 202  # from walk.png
        img_height = 248  # from walk.png
        for n in range(0, 8):  # eight images in walk.png by top to down (we use 0 column)
            single_image = sprt_map.subsurface((0, img_height * n, img_width, img_height))
            single_image = pygame.transform.smoothscale(single_image, (100, 100))  # here we make width and height = # 100 px
            self.animaList.append(single_image)

    def update(self, dx, dy):
        if dx == 0 and dy == 0:
            return
        self.anima_delay -= 1
        if self.anima_delay == 0:
            self.anima_pos += 1
            if self.anima_pos > 7:
                self.anima_pos = 0
            self.animateImg(dx, dy)
            self.anima_delay = globals.BOT_ANIMA_DELAY

    ###########################################################################
    # Function to implement sprite animation and sprite image rotation
    ###########################################################################
    def animateImg(self, dx, dy):

        vector = pygame.Vector2(dx, dy)
        y_axe = pygame.Vector2(0, 1)
        angle = vector.angle_to(y_axe)

        self.image = pygame.Surface((self.bot_width, self.bot_height))
        self.image.fill(globals.ZOOM_IN_WND_COLOR)
        self.image.blit(self.animaList[self.anima_pos], (0, 0))
        self.image = pygame.transform.rotate(self.image, angle + 180)
        if self.is_clicked:
            self.image = pygame.transform.smoothscale(self.image, (30, 30))
        self.rect = self.image.get_rect()  # get new rect after rotation!
    ###########################################################################
