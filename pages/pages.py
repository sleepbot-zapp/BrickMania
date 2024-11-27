class Page:
    def __init__(self, screen, height, width, scale, game) -> None:
        self.screen = screen
        self.height = height
        self.width = width
        self.scale = scale
        self.game = game

    def render_text(self, text, font, color, x, y, center=False, right_align=False):
        """Render text to the screen with alignment options."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            x -= text_rect.width // 2
        elif right_align:
            x -= text_rect.width
        self.screen.blit(text_surface, (x, y))
