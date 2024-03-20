import random

import pygame
import math
import globals
from random import randint


class SmallBot(pygame.sprite.Sprite):
    def __init__(self, small_bot_width, small_bot_height):
        super().__init__()
        self.bot_width = small_bot_width
        self.bot_height = small_bot_height

        self.image = pygame.Surface((self.bot_width, self.bot_height))
        self.image.fill(globals.MAIN_WND_COLOR)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, globals.RED, (self.bot_width / 2, self.bot_height / 2),
                           radius=globals.BOT_VISION_RADIUS, width=1)
        frame_rect = pygame.Rect(0, 0, globals.FRAME_WIDTH, globals.FRAME_HEIGHT)  # 4px X 4px by default
        frame_rect.center = self.rect.center
        pygame.draw.rect(self.image, globals.BLUE, frame_rect, width=1)

        self.given_speed_kmh = 5  # default speed
        self.delay = 0
        self.inc_px = 0

        self.hear_noise = False
        self.see = False

        self.bot_mode = globals.BOT_MODE_SEARCH
        self.direction = randint(1, 4)
        self.direction_time = 20  # parameter shows how long we do move to the given direction
        # increment for center x and y
        self.delta_x = 0
        self.delta_y = 0
        # sensors positions and intensity of noise
        self.coordinate_of_sensor = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.intensity_on_sensor = [0, 0, 0, 0]
        # angle to Y axe
        self.current_angle_to_Yaxe = None

        # bank of accumulators
        self.acc_x = 0
        self.acc_y = 0

        # flag if bot mode = to target
        self.bool_first_in = False

        # track
        self.track_list = []
        self.max_track_points = globals.MAX_TRACKS
        self.track_pause = globals.TRACK_PAUSE

        # range-meter
        self.range_meter = 0

        # behaviour flag
        self.is_attractive = True

        # printable status
        self.prt_status = ""

    def calc_sensors_position(self):
        # find sensor coordinates
        # 2px = 0.2m = 20sm
        self.coordinate_of_sensor[0] = [self.rect.centerx - 2, self.rect.centery - 2]
        self.coordinate_of_sensor[1] = [self.rect.centerx + 2, self.rect.centery - 2]
        self.coordinate_of_sensor[2] = [self.rect.centerx + 2, self.rect.centery + 2]
        self.coordinate_of_sensor[3] = [self.rect.centerx - 2, self.rect.centery + 2]

    def calc_trace(self):
        self.track_pause -= 1
        if self.track_pause == 0:
            self.track_pause = globals.TRACK_PAUSE
            self.track_list.append((self.rect.centerx, self.rect.centery))
            if len(self.track_list) > self.max_track_points:
                self.track_list = self.track_list[1:]

    def calc_range(self):
        range_in_pixels = math.sqrt((self.delta_x * self.delta_x) + (self.delta_y * self.delta_y))
        self.range_meter = self.range_meter + range_in_pixels / globals.PXLS_IN_METER

    @staticmethod
    def calc_inc_and_delay(given_speed_kmh):
        # we get speed in km/h and calc 1px increment by n frames(ticks). n = delay
        # see px_frames.xls
        speed_ms = given_speed_kmh * 1000 / 3600
        speed_px_s = speed_ms * globals.PXLS_IN_METER
        speed_px_s = round(speed_px_s, 0)
        round_delay = int(round(globals.FPS / speed_px_s, 0))
        round_px = int(round(speed_px_s / globals.FPS, 0))
        round_delay = 1 if round_delay < 1 else round_delay
        round_px = 1 if round_px < 1 else round_px
        return round_px, round_delay

    @staticmethod
    def get_whole_from_accu(accu_val):
        whole_part = int(accu_val)
        rest_part = accu_val - whole_part
        return whole_part, rest_part

    @staticmethod
    def calc_aver_intensity_point(sensors_coordinate_list, sensors_intensity_list):
        x_coordinate = 0
        y_coordinate = 0
        nominator_x = 0
        denominator = 0
        nominator_y = 0
        for point, intensity in zip(sensors_coordinate_list, sensors_intensity_list):
            nominator_x += point[0] * intensity
            nominator_y += point[1] * intensity
            denominator += intensity
        x_coordinate = nominator_x / denominator
        y_coordinate = nominator_y / denominator
        x_coordinate = round(x_coordinate, 3)
        y_coordinate = round(y_coordinate, 3)
        return (x_coordinate, y_coordinate)

    @staticmethod
    def angle2Yaxe(dx, dy):
        vector = pygame.Vector2(dx, dy)
        y_axe = pygame.Vector2(0, 1)
        angle = vector.angle_to(y_axe)
        return angle

    @staticmethod
    def distance_btw_points(point1, point2):
        distance = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        return distance

    def look(self, noise_center):
        radius = self.distance_btw_points(noise_center, self.rect.center)
        if radius < globals.BOT_VISION_RADIUS:
            self.see = True
        else:
            self.see = False

    def listen(self, noise_center):
        self.hear_noise = False
        self.calc_sensors_position()
        self.intensity_on_sensor = []  # empty intensity list
        for sensor_pos in self.coordinate_of_sensor:
            radius = self.distance_btw_points(noise_center, sensor_pos)
            radius = round(radius, 0)
            radius_meter = radius / globals.PXLS_IN_METER
            intensity = globals.Imax * math.exp(-radius_meter)
            if intensity >= globals.SENS_MIN:
                self.intensity_on_sensor.append(intensity)
                self.hear_noise = True
            else:
                self.intensity_on_sensor.append(0)

    def set_move_parameters(self):
        # generate random speed in km/h
        speed = 0
        while True:
            if speed == 0:
                speed = random.random() * 10
            else:
                break

        self.given_speed_kmh = speed
        speed = speed * 1000 / 3600  # turn km/h into m/s
        # generate random time in milliseconds
        time = randint(50, 1500)
        if self.bot_mode == globals.BOT_MODE_ESCAPE:
            time += 3000  # 3 seconds is panic_time (additional time for panic)
        # calc distance in meters
        distance = speed * (time / 10 ** 3)

        distance_px = round(distance * globals.PXLS_IN_METER, 0)
        frames = round(time * globals.FPS / 10 ** 3, 0)
        # how many frames to move
        self.delay = frames

        point = self.calc_aver_intensity_point(self.coordinate_of_sensor, self.intensity_on_sensor)
        if self.bot_mode == globals.BOT_MODE_ESCAPE:
            self.current_angle_to_Yaxe = self.angle2Yaxe((self.rect.centerx - point[0]),
                                                         (self.rect.centery - point[1]))
        else:
            self.current_angle_to_Yaxe = self.angle2Yaxe((point[0] - self.rect.centerx),
                                                         (point[1] - self.rect.centery))
        Xsum_px = distance_px * math.sin(math.radians(self.current_angle_to_Yaxe))
        Ysum_px = distance_px * math.cos(math.radians(self.current_angle_to_Yaxe))

        self.delta_x = Xsum_px / self.delay
        self.delta_y = Ysum_px / self.delay

    def update(self):
        ##################
        # SEARCH
        ##################
        if self.bot_mode == globals.BOT_MODE_SEARCH:
            # move randomizer
            if self.direction_time == 0:
                self.direction = randint(1, 4)
                self.direction_time = randint(20, 85)
            self.direction_time -= 1
            # move calculations
            if self.direction == globals.UP:
                self.delta_y = -self.inc_px
            elif self.direction == globals.DOWN:
                self.delta_y = self.inc_px
            elif self.direction == globals.LEFT:
                self.delta_x = -self.inc_px
            elif self.direction == globals.RIGHT:
                self.delta_x = self.inc_px

            # step out control
            if self.rect.right >= globals.WND_MAIN_WIDTH:
                self.direction = globals.LEFT
            if self.rect.left <= globals.SCREEN_WIDTH - globals.WND_MAIN_WIDTH:
                self.direction = globals.RIGHT
            if self.rect.top <= 0:
                self.direction = globals.DOWN
            if self.rect.bottom >= globals.WND_MAIN_HEIGHT:
                self.direction = globals.UP

            # move implementation for SEARCH
            if self.delay == 0:
                self.rect.centerx += self.delta_x
                self.rect.centery += self.delta_y

                self.calc_range()

                (self.inc_px, self.delay) = self.calc_inc_and_delay(self.given_speed_kmh)
            else:
                self.delay -= 1

            # we stop if heard something
            if self.hear_noise and self.bot_mode != globals.BOT_MODE_PAUSE:
                self.bot_mode = globals.BOT_MODE_PAUSE
                self.delay = globals.FPS  # STOP AFTER 1 second

        ##################
        # Pause Mode
        ##################

        if self.bot_mode == globals.BOT_MODE_PAUSE:
            self.delta_x = 0
            self.delta_y = 0
            if self.delay == 0:
                if self.is_attractive:
                    self.bot_mode = globals.BOT_MODE_TO_TARGET
                    self.bool_first_in = True
                else:
                    self.bot_mode = globals.BOT_MODE_ESCAPE
                    self.bool_first_in = True
            else:
                self.delay -= 1

        ##################
        # To Target
        ##################

        if self.bot_mode == globals.BOT_MODE_TO_TARGET:
            if self.delay == 0:
                if self.bool_first_in:
                    self.set_move_parameters()
                    self.bool_first_in = False
                else:
                    self.bot_mode = globals.BOT_MODE_PAUSE
                    self.delay = globals.FPS * 2

            else:
                if self.see:
                    self.bot_mode = globals.BOT_MODE_STOP
                    self.prt_status = "See!"
                    print(self.prt_status)
                self.acc_x += self.delta_x
                self.acc_y += self.delta_y

                whole_x, self.acc_x = self.get_whole_from_accu(self.acc_x)
                whole_y, self.acc_y = self.get_whole_from_accu(self.acc_y)
                self.rect.centerx += whole_x
                self.rect.centery += whole_y

                self.calc_range()

                self.delay -= 1

        ##################
        # ESCAPE
        ##################
        if self.bot_mode == globals.BOT_MODE_ESCAPE:
            if self.delay == 0:
                if self.bool_first_in:
                    self.set_move_parameters()
                    self.bool_first_in = False
                else:
                    self.bot_mode = globals.BOT_MODE_STOP
                    if self.hear_noise is False:
                        self.prt_status = "We are safe!"
                        print(self.prt_status)
            else:
                self.acc_x += self.delta_x
                self.acc_y += self.delta_y

                whole_x, self.acc_x = self.get_whole_from_accu(self.acc_x)
                whole_y, self.acc_y = self.get_whole_from_accu(self.acc_y)

                self.rect.centerx += whole_x
                self.rect.centery += whole_y

                self.calc_range()

                self.delay -= 1

        ##################
        # MODE STOP
        ##################

        if self.bot_mode == globals.BOT_MODE_STOP:
            self.delta_x = 0
            self.delta_y = 0
            self.delay = 0

        self.calc_trace()
