import socket
import threading
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def receive_messages(sock):
    """Receives messages from the server and prints them."""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break  # Server disconnected
            print(data.decode('utf-8'))
    except Exception as e:
        # If the error is due to socket shutdown, ignore it.
        if "10053" in str(e):
            pass
        else:
            print(f"Error receiving message: {e}")

def main():
    nickname = input("Choose a nickname: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")

            # Send nickname to the server
            s.sendall(nickname.encode('utf-8'))

            # Start a thread to receive messages from the server
            receive_thread = threading.Thread(target=receive_messages, args=(s,))
            receive_thread.daemon = True  # Allow the main thread to exit even if this is running
            receive_thread.start()

            while True:
                message = input("")  # Get input from the user
                if message.lower() == "quit":
                    s.shutdown(socket.SHUT_RDWR)
                    break  # Exit the loop if the user types 'quit'

                # Check for channel or private message commands
                if message.startswith("#"):
                    # Channel message: #channel_name message_text
                    pass  # We'll handle this on the server
                elif message.startswith("@"):
                    # Private message: @nickname message_text
                    pass  # We'll handle this on the server

                s.sendall(message.encode('utf-8'))

        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            print("Disconnected from server.")
            s.close()
            sys.exit() # Properly close the client

if __name__ == "__main__":
    main()

