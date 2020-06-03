import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to mangae bullets fired from Ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the Ship's Current Positon in screen"""

        super(Bullet, self).__init__()
        self.screen = screen

        # Creating a rectangle with ai_settings and properly determining position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Converting y-position for processing speed_factor of bullet
        self.y = float(self.rect.y)

        # Inheriting settings for bullet customization
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Update Bullet Trajectory"""

        self.y -= self.speed_factor

        # Update rectangle instance
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
