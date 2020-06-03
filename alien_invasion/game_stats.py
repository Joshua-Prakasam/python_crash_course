class GameStats:
    """Track Statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize Statistics"""
        self.score = 0
        self.ai_settings = ai_settings
        self.ships_left = None
        self.score = None
        self.level = None

        # Start Alien invasion in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

        self.reset_stats()

    def reset_stats(self):
        """Initialize Statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
