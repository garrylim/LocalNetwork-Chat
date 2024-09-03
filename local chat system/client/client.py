import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from plyer import notification

client_socket = None  # Initialize globally
running = False

def start_client():
    global client_socket, running
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip_entry.get(), 12346))
        display_message("Connected to the server.")
        running = True
        send_button.config(state=tk.NORMAL)  # Enable the send button once connected

        def receive_messages():
            while running:
                try:
                    message = client_socket.recv(1024).decode()
                    if not message:
                        break
                    display_message(f"Server: {message}")
                except Exception as e:
                    display_message(f"Error receiving message: {e}")
                    break
            client_socket.close()

        threading.Thread(target=receive_messages, daemon=True).start()

    except Exception as e:
        display_message(f"Connection failed: {e}")
        client_socket = None

def send_message(event=None):
    global client_socket
    if client_socket is None:
        display_message("Not connected to the server.")
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

def on_closing():
    global running, client_socket
    running = False
    if client_socket:
        client_socket.close()
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Client Chat")

tk.Label(root, text="Server IP/Name:").pack(padx=10, pady=5)
server_ip_entry = tk.Entry(root, width=40)
server_ip_entry.pack(padx=10, pady=5)
connect_button = tk.Button(root, text="Connect", command=start_client)
connect_button.pack(padx=10, pady=5)

chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, width=50, height=20)
chat_area.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5, side=tk.LEFT)
message_entry.bind("<Return>", send_message)  # Bind Enter key to send_message

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=5, side=tk.LEFT)
send_button.config(state=tk.DISABLED)  # Disable the send button initially

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
