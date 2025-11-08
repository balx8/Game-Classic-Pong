import os
import sys

def start_server():
    os.system(f'"{sys.executable}" server.py')

def start_client():
    os.system(f'"{sys.executable}" pong_client.py')

def main():
    while True:
        print("\n--- Pong Game ---")
        print("1. Run Server")
        print("2. Run Client")
        print("3. Exit")

        option = input("Choose an option: ").strip()

        if option == "1":
            start_server()
        elif option == "2":
            start_client()
        elif option == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
