import pygame

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

import game_functions as gf


def run_game():
    # Initialize Pygame, Settings and screen object
    pygame.init()
    pygame.display.set_caption("Alien Invasion")  # Setting Title

    # Setting Surface Size
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    score_board = Scoreboard(ai_settings, screen, stats)

    # Make a ship, group of aliens and group of bullets
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()

    # Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    while True:
        # watch for keyboard and mouse movements
        gf.check_events(ai_settings, screen, stats, score_board, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, score_board, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, score_board, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, score_board, ship, aliens, bullets, play_button)


run_game()
