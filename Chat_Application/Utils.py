# utils.py

def send_message_to_client(client, message):
    """
    Sends a message to a specific client.
    """
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message to client: {e}")

def broadcast_message(active_clients, message):
    """
    Sends a message to all connected clients.
    """
    for user in active_clients:
        send_message_to_client(user[1], message)

def remove_client(active_clients, client, username):
    """
    Removes a client from the active clients list and closes the connection.
    """
    client.close()
    active_clients.remove((username, client))
    print(f"Client {username} disconnected.")
    return f"CHATBOT ~{username} has left the chat."
