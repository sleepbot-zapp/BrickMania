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

    def update_db_highscore(self, mode, score):
        with self.game.session as conn:
            resp = conn.search(mode)
            highscore = score
            if resp["Response Code"] == 2:
                conn.add(mode, score)
            elif resp["Response"][mode] < score:
                conn.update(mode, score)
            else:
                highscore = resp["Response"][mode]
            return highscore

    def update_db_settings(self, mode, val):
        with self.game.session as conn:
            resp = conn.search(mode)
            if resp["Response Code"] == 2:
                conn.add(mode, val)
            else:
                conn.update(mode, val)
            conn.commit()
            print("nah", conn.show_all())
        return resp
