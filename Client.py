#imports
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import sys, os

#HOST = 'localhost'
PORT = 5579

BLACK = 'black'
DARK_GRAY = 'gray7'
WHITE = 'white'
DARK_BLUE = 'midnight blue'
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

#create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
running = True

def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + "\n")
    message_box.config(state=tk.DISABLED)

def connect():
    #connect to server
    ip = ip_textbox.get()
    try:
        client.connect((ip, PORT))
        add_message("Successfully Connected To Server")
    except:
        messagebox.showerror("Unable to connect to server",f"Unable to connect to server {ip} {PORT}")
    
    username = username_textbox.get()
    if username != '' or ip != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid Input", "Username cannot be empty\nIP cannot be blank and must be valid IP")
    
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)
    ip_textbox.config(state=tk.DISABLED)
    
    threading.Thread(target=listen_for_message_from_server, args=(client, )).start()

def disconnect():
    root.destroy()

def send_message():
    message = message_textbox.get()
    if message != "":
        client.sendall(message.encode())
        message_textbox.delete(0,len(message))
    else:
        messagebox.showerror("Invalid Input","Nothing to send or IP is not valid")

root = tk.Tk()
root.geometry("800x600")
root.title("Potato Chat")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", disconnect)
root.iconbitmap(resource("popoto.ico"))

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root,width=800,height=100,bg=BLACK)
top_frame.grid(row=0,column=0,sticky=tk.NSEW)

middle_frame = tk.Frame(root,width=800,height=400,bg=DARK_GRAY)
middle_frame.grid(row=1,column=0,sticky=tk.NSEW)

bottom_frame = tk.Frame(root,width=800,height=100,bg=BLACK)
bottom_frame.grid(row=2,column=0,sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter Username:", font=FONT, bg=BLACK, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=DARK_GRAY, fg=WHITE, width=15)
username_textbox.pack(side=tk.LEFT)

ip_label = tk.Label(top_frame, text="Enter IP:", font=FONT, bg=BLACK, fg=WHITE)
ip_label.pack(side=tk.LEFT, padx=10)

ip_textbox = tk.Entry(top_frame, font=FONT, bg=DARK_GRAY, fg=WHITE, width=15)
ip_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=DARK_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15,pady=5)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=DARK_GRAY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT,padx=10,pady=5)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=DARK_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=5, pady=5)

message_box = scrolledtext.ScrolledText(middle_frame,font=SMALL_FONT,bg=DARK_GRAY,fg=WHITE,width=89,height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

def listen_for_message_from_server(client):
    while 1:
        try:
            message = client.recv(2048).decode('utf-8')
        except:
            add_message("Disconnected from server\nRestart program if you want to reconnect to that sever")
            username_textbox.config(state=tk.NORMAL)
            username_button.config(state=tk.NORMAL)
            ip_textbox.config(state=tk.NORMAL)
            break
        if message != '':
            username = message.split("|")[0]
            content = message.split("|")[1]

            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Message received was empty","No message was received")

def main():
    root.mainloop()


if __name__ == '__main__':
    main()