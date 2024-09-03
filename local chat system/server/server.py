import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from plyer import notification

client_socket = None

def start_server():
    global client_socket
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('0.0.0.0', 12346))
            server_socket.listen(1)
            display_message("Server started, waiting for a connection...")
            
            client_socket, client_address = server_socket.accept()
            display_message(f"Connected to {client_address}")

            def receive_messages():
                global client_socket
                while True:
                    try:
                        message = client_socket.recv(1024).decode()
                        if not message:  # If the message is empty, the client has likely disconnected
                            break
                        display_message(f"Client: {message}")
                        show_notification("New Message", message)
                    except Exception as e:
                        display_message(f"Error receiving message: {e}")
                        break
                display_message("Client disconnected.")
                client_socket.close()
                client_socket = None
                server_socket.close()

            threading.Thread(target=receive_messages, daemon=True).start()

        except Exception as e:
            display_message(f"Server error: {e}")
            if client_socket:
                client_socket.close()
            server_socket.close()

def send_message(event=None):
    global client_socket
    if client_socket is None:
        display_message("No client connected.")
        return

    message = message_entry.get()
    if message:
        try:
            client_socket.send(message.encode())
            display_message(f"You: {message}")
            message_entry.delete(0, tk.END)
        except Exception as e:
            display_message(f"Error sending message: {e}")

def display_message(message):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"{message}\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )

def on_closing():
    global client_socket
    if client_socket:
        client_socket.close()
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Server Chat")

chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, width=50, height=20)
chat_area.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5, side=tk.LEFT)
message_entry.bind("<Return>", send_message)  # Bind Enter key to send_message

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=5, side=tk.LEFT)

threading.Thread(target=start_server, daemon=True).start()

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
