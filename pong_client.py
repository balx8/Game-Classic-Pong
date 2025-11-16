import pygame
import socket
import pickle
import threading


class PongClient:
    def __init__(self, host="localhost", port=5555):
        # --- Khởi tạo pygame ---
        pygame.init()
        pygame.mixer.init()

        # Âm thanh
        self.sound_hit = pygame.mixer.Sound("sounds/hit.wav")
        self.sound_score = pygame.mixer.Sound("sounds/score.wav")
        self.sound_hit.set_volume(1.0)
        self.sound_score.set_volume(1.0)

        # --- Kết nối tới server ---
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((host, port))
        except Exception as e:
            print(f"Khong the ket noi den server {host}:{port} - {e}")
            raise SystemExit

        # Nhận player_id từ server (0 hoặc 1)
        try:
            self.player_id = pickle.loads(self.client.recv(1024))
        except Exception as e:
            print("Loi khi nhan player_id tu server:", e)
            raise SystemExit

        print(f"Connected as Player {self.player_id + 1}")

        # --- Trạng thái game (nhận từ server) ---
        self.game_state = None
        self.prev_game_state = None
        self.running = True

        # Luật thắng
        self.max_score = 5
        self.game_over = False
        self.winner = 0  # 1 hoặc 2, 0 = hòa

        # --- Cửa sổ hiển thị ---
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Pong - Player {self.player_id + 1}")

        # Màu sắc
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Paddle local (chỉ lưu y, còn x cố định)
        self.paddle_y = 250
        self.paddle_speed = 5

        # Font
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

    # ---------------- Hàm nhận đúng n byte ----------------
    def recv_exact(self, n):
        """Nhận đúng n byte từ server (nếu không đủ thì trả về None)."""
        data = b""
        while len(data) < n and self.running:
            packet = self.client.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    # ---------------- Nhận game_state từ server ----------------
    def receive_game_state(self):
        while self.running:
            try:
                # Đọc 4 byte header (độ dài payload)
                header = self.recv_exact(4)
                if not header:
                    print("Server closed connection")
                    self.running = False
                    break

                length = int.from_bytes(header, "big")

                # Đọc đúng length byte dữ liệu pickle
                payload = self.recv_exact(length)
                if not payload:
                    print("Server closed connection (payload)")
                    self.running = False
                    break

                new_state = pickle.loads(payload)

                # --- PHÁT ÂM THANH DỰA TRÊN THAY ĐỔI GAME STATE ---
                if self.prev_game_state is not None:
                    old_ball = self.prev_game_state["ball"]
                    new_ball = new_state["ball"]

                    old_p1 = self.prev_game_state["paddle1"]
                    old_p2 = self.prev_game_state["paddle2"]
                    new_p1 = new_state["paddle1"]
                    new_p2 = new_state["paddle2"]

                    # 1) Score thay đổi -> tiếng ghi điểm
                    if (
                        old_p1["score"] != new_p1["score"]
                        or old_p2["score"] != new_p2["score"]
                    ):
                        self.sound_score.play()
                    else:
                        # 2) Hướng bóng đổi (dx đổi dấu) -> bóng vừa bật khỏi paddle
                        if old_ball["dx"] != new_ball["dx"]:
                            self.sound_hit.play()

                # --- Luật thắng: ai đạt max_score ---
                score1_val = new_state["paddle1"]["score"]
                score2_val = new_state["paddle2"]["score"]
                if not self.game_over and (
                    score1_val >= self.max_score or score2_val >= self.max_score
                ):
                    self.game_over = True
                    if score1_val > score2_val:
                        self.winner = 1
                    elif score2_val > score1_val:
                        self.winner = 2
                    else:
                        self.winner = 0  # hòa

                self.prev_game_state = new_state
                self.game_state = new_state

            except Exception as e:
                print("Connection lost:", e)
                self.running = False
                break

    # ---------------- Gửi vị trí paddle lên server ----------------
    def send_paddle_position(self):
        try:
            self.client.sendall(pickle.dumps(self.paddle_y))
        except Exception as e:
            print("Loi khi gui vi tri paddle:", e)
            self.running = False

    # ---------------- Vẽ khung hình ----------------
    def draw(self):
        self.screen.fill(self.BLACK)

        if self.game_state:
            pw = self.game_state["paddle_width"]
            ph = self.game_state["paddle_height"]

            # Đường giữa sân
            for i in range(0, self.height, 20):
                pygame.draw.rect(
                    self.screen,
                    self.WHITE,
                    (self.width // 2 - 2, i, 4, 10),
                )

            # Paddle trái (Player 1)
            pygame.draw.rect(
                self.screen,
                self.WHITE,
                (0, self.game_state["paddle1"]["y"], pw, ph),
            )

            # Paddle phải (Player 2)
            pygame.draw.rect(
                self.screen,
                self.WHITE,
                (self.width - pw, self.game_state["paddle2"]["y"], pw, ph),
            )

            # Bóng
            ball = self.game_state["ball"]
            pygame.draw.circle(
                self.screen,
                self.WHITE,
                (int(ball["x"]), int(ball["y"])),
                ball["radius"],
            )

            # Điểm số
            score1_val = self.game_state["paddle1"]["score"]
            score2_val = self.game_state["paddle2"]["score"]

            score1 = self.font.render(str(score1_val), True, self.WHITE)
            score2 = self.font.render(str(score2_val), True, self.WHITE)
            self.screen.blit(score1, (self.width // 4, 50))
            self.screen.blit(score2, (3 * self.width // 4, 50))

            # Gợi ý vị trí người chơi
            if self.player_id == 0:
                text = self.small_font.render("You (Left)", True, self.WHITE)
                self.screen.blit(text, (10, 10))
            else:
                text = self.small_font.render("You (Right)", True, self.WHITE)
                self.screen.blit(text, (self.width - 150, 10))

            # Nếu game_over thì vẽ overlay YOU WIN / YOU LOSE
            if self.game_over:
                if self.winner == 0:
                    msg = "DRAW!"
                elif self.winner == self.player_id + 1:
                    msg = "YOU WIN!"
                else:
                    msg = "YOU LOSE!"

                text_win = self.font.render(msg, True, self.WHITE)
                sub = self.small_font.render(
                    "Nhan ESC de thoat, mo lai client de choi van moi",
                    True,
                    self.WHITE,
                )

                rect = text_win.get_rect(center=(self.width // 2, self.height // 2))
                sub_rect = sub.get_rect(
                    center=(self.width // 2, self.height // 2 + 50)
                )

                overlay = pygame.Surface((self.width, self.height))
                overlay.set_alpha(150)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))

                self.screen.blit(text_win, rect)
                self.screen.blit(sub, sub_rect)

        else:
            # Đang chờ đối thủ
            text = self.font.render("Waiting for opponent...", True, self.WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    # ---------------- Vòng lặp chính của client ----------------
    def run(self):
        # Thread nhận game_state liên tục
        threading.Thread(target=self.receive_game_state, daemon=True).start()

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Cho phép nhấn ESC để thoát nhanh, nhất là khi game_over
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            # Chỉ cho điều khiển & gửi dữ liệu khi CHƯA game over
            if not self.game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and self.paddle_y > 0:
                    self.paddle_y -= self.paddle_speed
                if keys[pygame.K_DOWN] and self.paddle_y < self.height - 100:
                    self.paddle_y += self.paddle_speed

                self.send_paddle_position()

            # Vẽ khung hình
            self.draw()

            clock.tick(60)

        self.client.close()
        pygame.quit()


if __name__ == "__main__":
    client = PongClient()
    client.run()
