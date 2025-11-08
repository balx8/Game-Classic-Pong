import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.screen_height = screen_height

    def move(self):
        keys = pygame.key.get_pressed()

        # Điều khiển bằng cả W/S và ↑/↓
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed

        # Giữ vợt trong màn hình
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
