import pygame
import sys
import globals
from traces import Traces
from wnd_zoom_in import WndZoomIn
from koronka import Koronka
from value_view import ValueView
from noise_src import NoiseSrc
from wnd_main import WndMain
from bot import Bot
from small_bot import SmallBot
from random import randint
import math
import time


def main():
    pygame.init()  # pygame library start
    screen = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))  # creating the main screen
    screen.fill(globals.GREY)
    pygame.display.set_caption("Diploma")
    ico = pygame.image.load("ico.png")
    pygame.display.set_icon(ico)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()  # creating a group of drawable objects
    zoom_in_wnd = WndZoomIn(globals.WND_ZOOM_IN_WIDTH,
                            globals.WND_ZOOM_IN_HEIGHT)  # create zoom in window inside screen
    koronka = Koronka(globals.KORONKA_WIDTH, globals.KORONKA_HEIGHT)
    wnd_main = WndMain(globals.WND_MAIN_WIDTH, globals.WND_MAIN_HEIGHT)
    bot = Bot(globals.BOT_SIZE[0], globals.BOT_SIZE[1])  # create bot with given sizes
    noise_src = NoiseSrc(globals.NOISE_SIZE[0],
                         globals.NOISE_SIZE[1])  # create noise src object with given sizes to put on zoom in window

    small_bot = SmallBot(globals.SMALL_BOT_SIZE[0], globals.SMALL_BOT_SIZE[1])  # width, height 10 px = 1m
    small_bot.given_speed_kmh = 20
    small_bot.is_attractive = randint(0, 1)

    value_view = ValueView(globals.VALUE_VIEW_WIDTH, globals.VALUE_VIEW_HEIGHT)

    # random generation of the bot and the noise source.
    # check if the bot doesn't spawn in the noise source

    while True:
        noise_x_y = [randint(int(globals.WND_MAIN_WIDTH / 4), int(globals.WND_MAIN_WIDTH - globals.NOISE_SIZE[0])),
                     randint(int(globals.WND_MAIN_HEIGHT / 4), int(globals.WND_MAIN_HEIGHT - globals.NOISE_SIZE[1]))]
        noise_src.rect.center = (noise_x_y[0], noise_x_y[1])

        bot_x_y = [randint(int(globals.WND_MAIN_WIDTH / 4), int(globals.WND_MAIN_WIDTH - globals.SMALL_BOT_SIZE[0])),
                   randint(int(globals.WND_MAIN_HEIGHT / 4), int(globals.WND_MAIN_HEIGHT - globals.SMALL_BOT_SIZE[1]))]
        small_bot.rect.center = (bot_x_y[0], bot_x_y[1])

        if math.sqrt((noise_x_y[0] - bot_x_y[0]) ** 2 +
                     (noise_x_y[1] - bot_x_y[1]) ** 2) > (globals.NOISE_SIZE[0] / 2) + (globals.SMALL_BOT_SIZE[0] / 2):
            break

    all_sprites.add(zoom_in_wnd)
    all_sprites.add(koronka)
    all_sprites.add(wnd_main)

    trace_wnd = Traces(globals.WND_MAIN_WIDTH, globals.WND_MAIN_HEIGHT)

    count_time = 0
    time_point = time.time()

    # main program loop
    while True:
        clock.tick(globals.FPS)
        # get events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # check mouse click on bot window
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if zoom_in_wnd.rect.collidepoint(pos):
                    bot.is_clicked = not bot.is_clicked
        # render        
        # drawing group of sprites
        # zoom_in_wnd.image.blit(noise_src.image, (-20,-30)) # put noise src image on zoom in windows surface
        bot.rect.center = zoom_in_wnd.rect.center  # cool! center upper surface with underlay
        zoom_in_wnd.image.blit(bot.image, bot.rect)  # put bot image on zoom in windows surface

        # show traces
        trace_wnd.show_track(small_bot.track_list)

        # displaying draw things on the main window
        wnd_main.image.blit(noise_src.image, noise_src.rect)
        wnd_main.image.blit(trace_wnd.image, trace_wnd.rect)
        wnd_main.image.blit(small_bot.image, small_bot.rect)
        screen.blit(value_view.image, value_view.rect)

        # drawing the group of sprites
        all_sprites.draw(screen)

        # update all
        all_sprites.update()
        noise_src.update()
        small_bot.update()
        value_view.update(small_bot.intensity_on_sensor, small_bot.given_speed_kmh, small_bot.range_meter, count_time,
                          small_bot.is_attractive, small_bot.hear_noise, small_bot.prt_status, globals.SENS_MIN)
        bot.update(small_bot.delta_x, small_bot.delta_y)
        trace_wnd.update()

        # Listen for Noise
        small_bot.listen(noise_src.rect.center)
        small_bot.look(noise_src.rect.center)

        if small_bot.bot_mode != globals.BOT_MODE_STOP:
            delta_time = time.time() - time_point
            count_time = count_time + delta_time
            time_point = time.time()

        # display changes
        pygame.display.flip()


main()
