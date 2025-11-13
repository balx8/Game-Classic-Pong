import pygame

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color

    def update(self, screen_width, screen_height):
        """Cập nhật vị trí bóng và xử lý va chạm với tường"""
        self.x += self.speed_x
        self.y += self.speed_y

        # Va chạm tường trên/dưới
        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.speed_y = -self.speed_y

        # Va chạm tường trái/phải
        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.speed_x = -self.speed_x

    def draw(self, screen):
        """Vẽ bóng lên màn hình"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
