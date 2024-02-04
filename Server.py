#imports
import socket
import threading

you = socket.gethostname()
HOST = socket.gethostbyname(you)
PORT = 5579
LISTNER_LIMIT = 10
active_clients = [] #all currently online users

#listens for upcoming messages from client
def listen_for_message(client, username):
    while 1:
        message = ""
        try:
            message = client.recv(2048).decode('utf-8')
            if message != "":
                final_msg = username + "|" + message
                send_messages_to_all(final_msg)
            else:
                pass
        except:
            for user in active_clients:
                if user == (username,client):
                    active_clients.remove(user)
            client.close()
            break
    threading.Thread(target=client_handler, args=(client, )).start

#send message to everyone online
def send_messages_to_all(message):
    for user in active_clients:
        send_messages_to_client(user[1], message)

#send to a client
def send_messages_to_client(client, message):
    client.sendall(message.encode())

#send to handle client
def client_handler(client):
    #server listen for message and get username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != "":
            active_clients.append((username,client))
            join_msg = f"{username}| has joined the chat"
            send_messages_to_all(join_msg)
            break
        else:
            print("client username is empty")
    
    threading.Thread(target=listen_for_message, args=(client, username, )).start()

#main
def main():
    #create server socket class obj
    #AF_INET means use IPv4
    #SOCK_STREAM use TCP protocal
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server Started Successfully")
    print(f"IP is {HOST}")

    try:
        #provide server with address via host IP and Port
        server.bind((HOST, PORT))
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    #set server limit
    server.listen(LISTNER_LIMIT)

    #listens to client connection
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == "__main__":
    main()