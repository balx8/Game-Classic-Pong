import pygame


class Paddle:
    def __init__(self, x, y, width, height, speed, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.screen_height = screen_height

    @property
    def rect(self):
        """Trả về pygame.Rect đại diện cho paddle (dùng để va chạm)."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def _clamp(self):
        """Giữ vợt trong màn hình."""
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height

    def move_with_keys(self, keys, up_key, down_key):
        """Điều khiển paddle bằng bàn phím (vd: W/S hoặc ↑/↓)."""
        if keys[up_key]:
            self.y -= self.speed
        if keys[down_key]:
            self.y += self.speed
        self._clamp()

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))


def move_ai_paddle(paddle: Paddle, ball_y: float, ai_speed: float):
    """
    Điều khiển paddle bằng AI (đuổi theo bóng).

    ai_speed: tốc độ riêng của AI (có thể khác speed của paddle).
    """
    center_y = paddle.y + paddle.height / 2

    if center_y < ball_y:
        paddle.y += ai_speed
    elif center_y > ball_y:
        paddle.y -= ai_speed

    # giữ trong màn hình
    if paddle.y < 0:
        paddle.y = 0
    elif paddle.y + paddle.height > paddle.screen_height:
        paddle.y = paddle.screen_height - paddle.height
