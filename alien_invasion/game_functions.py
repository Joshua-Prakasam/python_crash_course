import sys
import pygame as pyg

from time import sleep
from bullet import Bullet
from alien import Alien


def fire_bullet(ai_settings, screen, ship, bullets):
    # Create a new bullet and add them in bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_key_up_events(event, ai_settings, screen, ship, bullets):
    """Respond to Key Up Events"""

    if event.key == pyg.K_LEFT:
        ship.moving_left = True
    elif event.key == pyg.K_RIGHT:
        ship.moving_right = True
    elif event.key == pyg.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def check_key_down_events(event, ship):
    """Respond to Key Down Events"""
    if event.key == pyg.K_LEFT:
        ship.moving_left = False
    elif event.key == pyg.K_RIGHT:
        ship.moving_right = False


def get_numbers_alien_x(ai_settings, alien_width):
    """Determine the Number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    numbers_alien_x = int(available_space_x / (2 * alien_width))
    return numbers_alien_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the Number of aliens that fit on the screen"""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + (2 * alien_width * alien_number)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""

    # Finding Aliens in a row by calculation
    # Spacing for each alien and margin of screen are equal to one alien width
    alien = Alien(ai_settings, screen)
    numbers_alien_x = get_numbers_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        # Create row of aliens and add it to the aliens
        for alien_number in range(numbers_alien_x):
            # Create an alien and place it in ro
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_play_button(ai_settings, screen, stats, score_board, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pyg.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        score_board.prep_score()
        score_board.prep_high_score()
        score_board.prep_level()
        score_board.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)


def check_events(ai_settings, screen, stats, score_board, play_button, ship, aliens, bullets):
    """Respond to key press and mouse events"""
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            sys.exit()
        elif event.type == pyg.KEYDOWN:
            check_key_up_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pyg.KEYUP:
            check_key_down_events(event, ship)
        elif event.type == pyg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pyg.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, score_board, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings, screen: pyg.SurfaceType, stats, score_board, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen"""
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw the Score information.
    score_board.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pyg.display.flip()


def check_bullet_alien_collision(ai_settings, screen, stats, score_board, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pyg.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            score_board.prep_score()
        check_high_score(stats, score_board)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        score_board.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def update_bullets(ai_settings, screen, stats, score_board, ship, aliens, bullets):
    """Update Bullet and remove old bullets"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, stats, score_board, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_directions(ai_settings, aliens)
            break


def change_fleet_directions(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, score_board, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
        and then update the position of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pyg.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, score_board, ship, aliens, bullets)

    # Look for the aliens hitting the bottom screen
    check_aliens_bottom(ai_settings, stats, screen, score_board, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, score_board, ship, aliens, bullets):
    """Respond to ship hit by alien."""

    if stats.ships_left > 0:
        # Decrement ship left
        stats.ships_left -= 1

        # Update scoreboard.
        score_board.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause for half second.
        sleep(0.5)

    else:
        stats.game_active = False
        stats.score = 0
        pyg.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, score_board, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the Screen."""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, score_board, ship, aliens, bullets)
            break


def check_high_score(stats, score_board):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score_board.prep_high_score()