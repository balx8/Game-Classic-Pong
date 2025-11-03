from pong_server import PongServer

def main():
    print("🚀 Starting Pong Server...")
    server = PongServer(host='localhost', port=5555)
    server.start()

if __name__ == "__main__":
    main()
