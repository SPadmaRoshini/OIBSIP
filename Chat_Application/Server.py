import socket
import threading
from utils import send_message_to_client, broadcast_message, remove_client  # Import functions from utils.py

HOST = '127.0.0.1'
PORT = 1489
LIMIT = 10
active_clients = []

def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                final_msg = f"{username}~{message}"
                broadcast_message(active_clients, final_msg)
            else:
                print(f"Received empty message from {username}. Closing connection.")
                leave_message = remove_client(active_clients, client, username)
                broadcast_message(active_clients, leave_message)
                break
        except Exception as e:
            print(f"Error receiving message from {username}: {e}")
            leave_message = remove_client(active_clients, client, username)
            broadcast_message(active_clients, leave_message)
            break

def client_handler(client):
    while True:
        try:
            username = client.recv(2048).decode('utf-8')
            if username:
                active_clients.append((username, client))
                welcome_message = f"CHATBOT ~{username} joined the chat"
                broadcast_message(active_clients, welcome_message)
                break
            else:
                print("Received empty username. Requesting again.")
        except Exception as e:
            print(f"Error receiving username: {e}")
            break

    threading.Thread(target=listen_for_messages, args=(client, username,)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} on port {PORT}: {e}")
        return

    server.listen(LIMIT)
    print("Server is listening for connections...")

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]}:{address[1]}")
        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()
