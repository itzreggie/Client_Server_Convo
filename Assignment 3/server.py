import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

clients = {}  # Dictionary to store client connections and nicknames
channels = {} # Dictionary to store channels and the clients in them

def broadcast_all(message, sender_conn):
    """Broadcasts a message to all connected clients regardless of channel."""
    for client_conn in clients:
        if client_conn != sender_conn:
            try:
                client_conn.sendall(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                client_channel = clients[client_conn]["channel"]
                leave_channel(client_conn, client_channel)
                del clients[client_conn]

def handle_client(conn, addr):
    """Handles individual client connections."""
    try:
        nickname = conn.recv(1024).decode('utf-8')
        print(f"Client {addr} chose nickname: {nickname}")
        # Set default channel to general (which always exists)
        clients[conn] = {"nickname": nickname, "channel": "general"}
        join_channel(conn, "general")
        broadcast(f"{nickname} has joined the chat!".encode('utf-8'), conn, "general")

        while True:
            data = conn.recv(1024)
            if not data:
                break  # Client disconnected
            message = data.decode('utf-8')
            print(f"Received from {nickname} ({addr}): {message}")

            # Allow user to switch channel using /join command
            if message.startswith("/join "):
                new_channel = message.split(" ", 1)[1].strip()
                old_channel = clients[conn]["channel"]
                # For channels other than "general", require that the channel already exists
                if new_channel != "general" and new_channel not in channels:
                    try:
                        conn.sendall(f"Server: Channel '{new_channel}' does not exist. You cannot join it."
                                     .encode("utf-8"))
                    except Exception as e:
                        print(f"Error sending message: {e}")
                    continue
                # Inform the old channel that the user is leaving
                broadcast(f"{nickname} has left channel {old_channel}".encode('utf-8'), conn, old_channel)
                leave_channel(conn, old_channel)
                # Join the new channel and broadcast the event
                join_channel(conn, new_channel)
                broadcast(f"{nickname} has joined channel {new_channel}".encode('utf-8'), conn, new_channel)
                try:
                    conn.sendall(f"Server: You joined channel {new_channel}".encode("utf-8"))
                except Exception as e:
                    print(f"Error sending join confirmation: {e}")

            elif message.startswith("#"):
                parts = message.split(" ", 1)
                if len(parts) > 1:
                    channel_name = parts[0][1:]  # Remove '#' to get channel name
                    message_text = parts[1]
                    newly_created = False
                    # If channel doesn't exist yet, create it when someone sends a message there.
                    if channel_name not in channels:
                        channels[channel_name] = []
                        # Automatically join the sender to the new channel
                        join_channel(conn, channel_name)
                        newly_created = True
                    broadcast(f"{nickname} (Channel {channel_name}): {message_text}".encode('utf-8'),
                              conn, channel_name)
                    if newly_created:
                        creation_msg = f"Server: Channel '{channel_name}' was created by {nickname}. {message_text}"
                        broadcast_all(creation_msg.encode('utf-8'), conn)

            elif message.startswith("@"):
            # Private message: @nickname message_text
                parts = message.split(" ", 1)
                if len(parts) > 1:
                    recipient_nickname = parts[0][1:]  # Remove '@'
                    message_text = parts[1]
                    send_private_message(f"{nickname} (Private): {message_text}".encode('utf-8'),
            # Default: send to client's current channel
                                         conn, recipient_nickname)
            else:
            # Default: send to client's current channel
                current_channel = clients[conn]["channel"]
                broadcast(f"{nickname}: {message}".encode('utf-8'), conn, current_channel)

    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        nickname = clients.get(conn, {}).get("nickname")
        if nickname:
            channel = clients[conn]["channel"]
            leave_channel(conn, channel)
            broadcast(f"{nickname} has left the chat.".encode('utf-8'), conn, channel)
        print(f"Disconnected from {addr}")
        del clients[conn]
        conn.close()

def broadcast(message, sender_conn, channel_name):
    """Broadcasts a message to all clients in a channel except the sender."""
    for client_conn, client_data in clients.items():
        if client_conn != sender_conn and client_data["channel"] == channel_name:
            try:
                client_conn.sendall(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                # Remove the client if there's an error
                leave_channel(client_conn, channel_name)
                del clients[client_conn]

def send_private_message(message, sender_conn, recipient_nickname):
    """Sends a private message to a specific client."""
    for client_conn, client_data in clients.items():
        if client_data["nickname"] == recipient_nickname:
            try:
                client_conn.sendall(message)
                return  # Message sent, exit the loop
            except Exception as e:
                print(f"Error sending private message: {e}")
                # Remove the client if there's an error
                channel = clients[client_conn]["channel"]
                leave_channel(client_conn, channel)
                del clients[client_conn]
                return

    # If the recipient is not found
    sender_nickname = clients[sender_conn]["nickname"]
    try:
        sender_conn.sendall(f"Server: User {recipient_nickname} not found.".encode('utf-8'))
    except:
        print("could not send message to the client")

def join_channel(conn, channel_name):
    """Adds a client to a channel.
       For 'general', the channel is created if it doesn't exist.
       Other channels must already exist."""
    if channel_name == "general":
        if channel_name not in channels:
            channels[channel_name] = []
        channels[channel_name].append(conn)
        clients[conn]["channel"] = "general"
    else:
        if channel_name in channels:
            channels[channel_name].append(conn)
            clients[conn]["channel"] = channel_name
        else:
            # Raise an error (or handle it in the /join section) if the channel does not exist.
            raise ValueError(f"Channel {channel_name} does not exist.")

def leave_channel(conn, channel_name):
    """Removes a client from a channel."""
    if channel_name in channels and conn in channels[channel_name]:
        channels[channel_name].remove(conn)

def main():
    """Sets up the server and listens for connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()