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
        """Cập nhật vị trí bóng và xử lý va chạm với tường TRÊN/DƯỚI"""
        self.x += self.speed_x
        self.y += self.speed_y

        # Va chạm tường trên/dưới
        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.speed_y = -self.speed_y

        # Lưu ý: KHÔNG xử lý tường trái/phải ở đây
        # để main.py còn tính điểm khi bóng ra ngoài.

    def reset(self, screen_width, screen_height, direction=1):
        """Đưa bóng về giữa sân, đổi hướng theo direction (-1 hoặc 1)"""
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.speed_x = abs(self.speed_x) * direction
        # cho speed_y về dương, sau đó sẽ đổi hướng nếu muốn
        self.speed_y = abs(self.speed_y)

    def draw(self, screen):
        """Vẽ bóng lên màn hình"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
