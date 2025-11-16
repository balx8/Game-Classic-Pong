import socket
import threading
import pickle
import time


class PongServer:
    def __init__(self, host="localhost", port=5555):
        # Tạo socket TCP/IP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"Server started on {host}:{port}")

        # Trạng thái game ban đầu
        self.game_state = {
            "ball": {"x": 400, "y": 300, "dx": 2, "dy": 2, "radius": 10},  # chậm hơn
            "paddle1": {"y": 250, "score": 0},
            "paddle2": {"y": 250, "score": 0},
            "width": 800,
            "height": 600,
            "paddle_width": 10,
            "paddle_height": 100,
        }

        self.clients = []          # danh sách socket client
        self.running = True
        self.game_started = False

    # ---------------- Xử lý từng client ----------------
    def handle_client(self, conn, player_id: int):
        print(f"Player {player_id} connected")
        # gửi player_id cho client biết mình là player 0 hay 1
        conn.send(pickle.dumps(player_id))

        while self.running:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                # nhận vị trí paddle từ client
                paddle_y = pickle.loads(data)
                if player_id == 0:
                    self.game_state["paddle1"]["y"] = paddle_y
                else:
                    self.game_state["paddle2"]["y"] = paddle_y

            except Exception as e:
                print(f"Error with player {player_id}: {e}")
                break

        # client out
        try:
            conn.close()
        except Exception:
            pass

        if conn in self.clients:
            self.clients.remove(conn)

        print(f"Player {player_id} disconnected")

    # ---------------- Cập nhật logic game ----------------
    def update_game(self):
        """Vòng lặp cập nhật vị trí bóng, xử lý va chạm, tính điểm."""
        while self.running:
            if len(self.clients) == 2 and self.game_started:
                ball = self.game_state["ball"]

                # cập nhật vị trí bóng
                ball["x"] += ball["dx"]
                ball["y"] += ball["dy"]

                # Va chạm tường trên/dưới
                if (
                    ball["y"] <= ball["radius"]
                    or ball["y"] >= self.game_state["height"] - ball["radius"]
                ):
                    ball["dy"] *= -1

                # Va chạm với paddle
                p1 = self.game_state["paddle1"]
                p2 = self.game_state["paddle2"]
                pw = self.game_state["paddle_width"]
                ph = self.game_state["paddle_height"]

                # Paddle trái
                if (
                    ball["x"] - ball["radius"] <= pw
                    and p1["y"] <= ball["y"] <= p1["y"] + ph
                ):
                    ball["dx"] = abs(ball["dx"])

                # Paddle phải
                if (
                    ball["x"] + ball["radius"] >= self.game_state["width"] - pw
                    and p2["y"] <= ball["y"] <= p2["y"] + ph
                ):
                    ball["dx"] = -abs(ball["dx"])

                # Ghi điểm
                if ball["x"] <= 0:
                    p2["score"] += 1
                    self.reset_ball()
                elif ball["x"] >= self.game_state["width"]:
                    p1["score"] += 1
                    self.reset_ball()

            time.sleep(0.033)  # ~30 FPS, đỡ giật hơn

    def reset_ball(self):
        """Đưa bóng về giữa sân sau khi có điểm."""
        ball = self.game_state["ball"]
        ball["x"] = 400
        ball["y"] = 300
        # Giữ nguyên hướng ngang hiện tại (dương/âm), nhưng tốc độ chậm hơn
        ball["dx"] = 2 if ball["dx"] > 0 else -2
        ball["dy"] = 2

    # ---------------- Gửi trạng thái game cho client ----------------
    def send_state_to_client(self, client):
        """Gửi game_state cho 1 client với header 4 byte độ dài."""
        try:
            payload = pickle.dumps(self.game_state, protocol=pickle.HIGHEST_PROTOCOL)
            header = len(payload).to_bytes(4, "big")  # 4 byte big-endian
            client.sendall(header + payload)
        except Exception as e:
            print(f"Loi khi gui data cho client: {e}")
            if client in self.clients:
                self.clients.remove(client)

    def broadcast_game_state(self):
        """Broadcast game_state cho tất cả client ~30 FPS."""
        while self.running:
            if len(self.clients) == 2:
                if not self.game_started:
                    self.game_started = True
                    print("Game started!")

                for client in self.clients[:]:
                    self.send_state_to_client(client)

            time.sleep(0.033)  # ~30 FPS

    # ---------------- Hàm start server chính ----------------
    def start(self):
        # Thread cập nhật game
        threading.Thread(target=self.update_game, daemon=True).start()

        # Thread broadcast trạng thái game
        threading.Thread(target=self.broadcast_game_state, daemon=True).start()

        print("Waiting for players...")

        # Chấp nhận tối đa 2 client
        player_id = 0
        while self.running and len(self.clients) < 2:
            conn, addr = self.server.accept()
            print(f"New connection from {addr}")
            self.clients.append(conn)
            threading.Thread(
                target=self.handle_client,
                args=(conn, player_id),
                daemon=True,
            ).start()
            player_id += 1

        # Giữ server chạy cho tới khi Ctrl+C
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.running = False
            self.server.close()


if __name__ == "__main__":
    server = PongServer()
    server.start()
