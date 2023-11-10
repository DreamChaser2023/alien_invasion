import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        """Initialize the button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.base_color = (0, 135, 0)
        self.base_color = (0, 255, 255)
        self.highlight_color = (0, 65, 0)
        self.msg = msg

        self.width, self.height = 200, 50
        self.button_color = self.base_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg()

    def _prep_msg(self):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _update_msg_position(self):
        self.msg_image_rect.center = self.rect.center

    def set_highlighted_color(self):
        self.button_color = self.highlight_color
        self._prep_msg()

    def set_base_color(self):
        self.button_color = self.base_color
        self._prep_msg()

    def draw_button(self):
        """Draw the button at its current location."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)