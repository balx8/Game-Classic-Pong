import pygame
import socket
import pickle
import threading


class PongClient:
    def __init__(self, host='localhost', port=5555):
        # Initialize pygame
        pygame.init()

        # Connect to server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.player_id = pickle.loads(self.client.recv(1024))
        print(f"Connected as Player {self.player_id + 1}")

        # Game state
        self.game_state = None
        self.running = True

        # Display
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Pong - Player {self.player_id + 1}")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Paddle control
        self.paddle_y = 250
        self.paddle_speed = 5

        # Font
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

    def receive_game_state(self):
        while self.running:
            try:
                data = self.client.recv(4096)
                if data:
                    self.game_state = pickle.loads(data)
            except:
                print("Connection lost")
                self.running = False
                break

    def send_paddle_position(self):
        try:
            self.client.send(pickle.dumps(self.paddle_y))
        except:
            self.running = False

    def draw(self):
        self.screen.fill(self.BLACK)

        if self.game_state:
            # Draw center line
            for i in range(0, self.height, 20):
                pygame.draw.rect(self.screen, self.WHITE,
                                 (self.width // 2 - 2, i, 4, 10))

            # Draw paddles
            pw = self.game_state['paddle_width']
            ph = self.game_state['paddle_height']

            # left paddle (Player 1)
            pygame.draw.rect(self.screen, self.WHITE,
                             (0, self.game_state['paddle1']['y'], pw, ph))

            # right paddle (Player 2)
            pygame.draw.rect(self.screen, self.WHITE,
                             (self.width - pw, self.game_state['paddle2']['y'], pw, ph))

            # Draw ball
            ball = self.game_state['ball']
            pygame.draw.circle(self.screen, self.WHITE,
                               (int(ball['x']), int(ball['y'])), ball['radius'])

            # draw scores
            score1 = self.font.render(str(self.game_state['paddle1']['score']),
                                      True, self.WHITE)
            score2 = self.font.render(str(self.game_state['paddle2']['score']),
                                      True, self.WHITE)
            self.screen.blit(score1, (self.width // 4, 50))
            self.screen.blit(score2, (3 * self.width // 4, 50))

            # Draw player indicator
            if self.player_id == 0:
                text = self.small_font.render("You (Left)", True, self.WHITE)
                self.screen.blit(text, (10, 10))
            else:
                text = self.small_font.render("You (Right)", True, self.WHITE)
                self.screen.blit(text, (self.width - 150, 10))
        else:
            # Waiting for opponent
            text = self.font.render(
                "Waiting for opponent...", True, self.WHITE)
            text_rect = text.get_rect(
                center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        # Start receiving thread
        threading.Thread(target=self.receive_game_state, daemon=True).start()

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.paddle_y > 0:
                self.paddle_y -= self.paddle_speed
            if keys[pygame.K_DOWN] and self.paddle_y < self.height - 100:
                self.paddle_y += self.paddle_speed

            # Send paddle position to server
            self.send_paddle_position()

            # Draw everything
            self.draw()

            clock.tick(60)

        self.client.close()
        pygame.quit()


if __name__ == "__main__":
    client = PongClient()
    client.run()
