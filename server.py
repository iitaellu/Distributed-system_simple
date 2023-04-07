"""
https://www.youtube.com/watch?v=F_JDA96AdEI&t=254s
https://www.youtube.com/watch?v=3UOyky9sEQY

"""


import threading
import socket

# Connection Data
host = '127.0.0.1'
port = 3000

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames and list of rooms
clients = []
nicknames = []
rooms = ['JavaScript', 'C/C#', 'Python']

# Sending Messages To All Connected Clients
def broadcast(msg):
    for client in clients:
        client.send(msg)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            print(msg)
            print(nicknames)
            # Check if something what user wants to do
            #Kick named user out of chat
            if msg.decode('ascii').startswith('KICK'):
                name_to_kick = msg.decode('ascii')[5:]
                print("Hello")
                kick_user(name_to_kick)
            # Prints out rooms user can choose
            elif msg.decode('ascii').startswith('ROOMS'):
                print(rooms)
                name = msg.decode('ascii')[6:]
                print(name)
                printRooms(name)
            # Print online Clients out
            elif msg.decode('ascii').startswith('ONLINE'):
                name = msg.decode('ascii')[7:]
                printClients(name)
            # Print menu
            elif msg.decode('ascii').startswith('HELP'):
                name = msg.decode('ascii')[5:]
                printMenu(name)
            #Private messages
            elif msg.decode('ascii').startswith('PRIVATE'):
                names = msg.decode('ascii')[8:]
                details = names.split(" ")
                sender = details[0]
                recipient = details[1]
                privatemsg = msg.decode('ascii')[8+len(sender)+len(recipient)+2:]
                sendPrivate(sender, recipient, privatemsg)
            # Broadcasting Messages
            else:
                broadcast(message)
            
             
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break
            """
                break
            elif msg.decode('ascii').startswith('PRIVATE'):
                name_to_private = msg.decode('ascii'[8:])
                pass    
            elif msg.decode('ascii').startswith('LEAVE'):
                    name = msg.decode('ascii')[6:]
                    print(name)
                    leaveChat(name)
            """
            
            """if(message[len(nickname)+2:] == "quit"):
                index = clients.index(client)
                client.send("leave from chat")
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break
            else:
                broadcast(message)"""

def menu():
     message = '\n\n***********_MENU_*********\nType "/help" to see menu\nType "/kick (name)" to kick out\nType "/rooms" to see topic rooms\nType "/online" to see client online\nType "/private (name) (message)" to send private message\nLeave chat by pressing ctrl + C\n***************************'
     return message
    
# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

         # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(f"Nickname of clients is {nickname}!")
        broadcast(f'{nickname} joined to chat!'.encode('ascii'))

        client.send('Connected to the server!'.encode('ascii'))
        message = menu()
        client.send(f'{message}'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    print(name)
    #If user in nicnames then kick out from room
    if name in nicknames:
        name_index = nicknames.index(name)
        nicknames.remove(name)
        
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        broadcast(f'{name} was kicked out'.encode('ascii'))
        client_to_kick.send("You were kicked out".encode('ascii'))
        client_to_kick.close()
        
        
def findClient(name):
    for i in nicknames:
        name_index = nicknames.index(i)
        client= clients[name_index]
        return client
    
# Prints list of rooms()
def printRooms(names):
    for i in nicknames:
        if(str(i) == str(names)):
            print("True")
            name_index = nicknames.index(i)
            client_for_show = clients[name_index]
            print(client_for_show)
            client_for_show.send(f" The rooms to choose {rooms}".encode('ascii'))

# Prints list of clients
def printClients(names):
    print(names+'!')
    for i in nicknames:
        if(str(i) == str(names)):
            print("True")
            name_index = nicknames.index(i)
            client_for_show = clients[name_index]
            print(client_for_show)
            client_for_show.send(f" On the server {nicknames}".encode('ascii'))

def printMenu(name):
    print(name)
    if name in nicknames:
        name_index = nicknames.index(name)
        client_for_menu = clients[name_index]
        message = menu()
        client_for_menu.send(f"{message}".encode('ascii'))

#Private messages
def sendPrivate(sender, recipient, msg):
    if recipient in nicknames:
        name_index = nicknames.index(recipient)        
        client_to_send = clients[name_index]
        client_to_send.send(f"{sender} (Private): {msg}".encode('ascii'))

#Leave from chat
def leaveChat(name):
    print('Hello')

    name_index = nicknames.index(name)
    nicknames.remove(name)
    client_to_leave = clients[name_index]
    clients.remove(client_to_leave)
    broadcast(f'{name} left the chat'.encode('ascii'))
    client_to_leave.send("You left the chat".encode('ascii'))
    client_to_leave.close()
    
    
    
    


print("Server is listening...")
receive()
