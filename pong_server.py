import socket
import threading
import pickle
import time


class PongServer:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"Server started on {host}:{port}")

        # Game state
        self.game_state = {
            'ball': {'x': 400, 'y': 300, 'dx': 3, 'dy': 3, 'radius': 10},
            'paddle1': {'y': 250, 'score': 0},
            'paddle2': {'y': 250, 'score': 0},
            'width': 800,
            'height': 600,
            'paddle_width': 10,
            'paddle_height': 100
        }

        self.clients = []
        self.running = True
        self.game_started = False

    def handle_client(self, conn, player_id):
        print(f"Player {player_id} connected")
        conn.send(pickle.dumps(player_id))

        while self.running:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                # receive paddle position from client
                paddle_y = pickle.loads(data)
                if player_id == 0:
                    self.game_state['paddle1']['y'] = paddle_y
                else:
                    self.game_state['paddle2']['y'] = paddle_y

            except:
                break

        conn.close()
        self.clients.remove(conn)
        print(f"Player {player_id} disconnected")

    def update_game(self):
        while self.running:
            if len(self.clients) == 2 and self.game_started:
                ball = self.game_state['ball']

                # update ball position
                ball['x'] += ball['dx']
                ball['y'] += ball['dy']

                # Ball collision with top/bottom
                if ball['y'] <= ball['radius'] or ball['y'] >= self.game_state['height'] - ball['radius']:
                    ball['dy'] *= -1

                # Ball collision with paddles
                p1 = self.game_state['paddle1']
                p2 = self.game_state['paddle2']
                pw = self.game_state['paddle_width']
                ph = self.game_state['paddle_height']

                # Left paddle collision
                if (ball['x'] - ball['radius'] <= pw and
                        p1['y'] <= ball['y'] <= p1['y'] + ph):
                    ball['dx'] = abs(ball['dx'])

                # Right paddle collision
                if (ball['x'] + ball['radius'] >= self.game_state['width'] - pw and
                        p2['y'] <= ball['y'] <= p2['y'] + ph):
                    ball['dx'] = -abs(ball['dx'])

                # Scoring
                if ball['x'] <= 0:
                    p2['score'] += 1
                    self.reset_ball()
                elif ball['x'] >= self.game_state['width']:
                    p1['score'] += 1
                    self.reset_ball()

            time.sleep(0.016)  # ~60 FPS

    def reset_ball(self):
        ball = self.game_state['ball']
        ball['x'] = 400
        ball['y'] = 300
        ball['dx'] = 3 if ball['dx'] > 0 else -3
        ball['dy'] = 3

    def broadcast_game_state(self):
        while self.running:
            if len(self.clients) == 2:
                if not self.game_started:
                    self.game_started = True
                    print("Game started!")

                data = pickle.dumps(self.game_state)
                for client in self.clients[:]:
                    try:
                        client.send(data)
                    except:
                        self.clients.remove(client)

            time.sleep(0.016)  # ~60 FPS

    def start(self):
        # Start game update thread
        threading.Thread(target=self.update_game, daemon=True).start()

        # Start broadcast thread
        threading.Thread(target=self.broadcast_game_state, daemon=True).start()

        # kccept clients
        player_id = 0
        while self.running and len(self.clients) < 2:
            conn, addr = self.server.accept()
            self.clients.append(conn)
            threading.Thread(target=self.handle_client, args=(
                conn, player_id), daemon=True).start()
            player_id += 1

        print("Waiting for players...")

        # keep server running
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
