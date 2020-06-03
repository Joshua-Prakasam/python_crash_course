import pygame
from pygame import SurfaceType


class Ship(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its position"""
        super(Ship, self).__init__()
        self.screen: SurfaceType = screen  # type
        self.ai_settings = ai_settings

        # Load the ship image and get the rectangle (Background Occupation)
        self.image: SurfaceType = pygame.image.load('./images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom of the screen
        self.rect.centerx = float(self.screen_rect.centerx)
        self.rect.bottom = self.screen_rect.bottom

        # Flags for movement monitoring
        self.moving_right = False
        self.moving_left = False

        # Setting Decimal Value for center
        self.center = float(self.rect.centerx)

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update ship movements according to Flags"""
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        elif self.moving_right and self.rect.right < self.screen.get_width():
            self.center += self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
