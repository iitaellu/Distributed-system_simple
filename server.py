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
            # Check if something what user wants to do
            #Kick named user out of chat
            if msg.decode('ascii').startswith('KICK'):
                name_to_kick = msg.decode('ascii')[5:]
                names = msg.decode('ascii')[5:]
                details = names.split(" ")
                sender = details[0]
                kick = details[1]
                kick_user(sender, kick)
            # Prints out rooms user can choose
            elif msg.decode('ascii').startswith('ROOMS'):
                name = msg.decode('ascii')[6:]
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
            #Go room
            elif msg.decode('ascii').startswith('GOROOM'):
                names = msg.decode('ascii')[7:]
                details = names.split(" ")
                sender = details[0]
                room = details[1]
                goRoom(sender, room)
            #Go private room with friend
            elif msg.decode('ascii').startswith('GOPRIVATE'):
                names = msg.decode('ascii')[10:]
                print(names)
                details = names.split(" ")
                sender = details[0]
                buddy = details[1]
                goPrivate(sender, buddy)
                """
                elif msg.decode('ascii').startswith('LEAVE'):
                    name = msg.decode('ascii')[6:]
                    print(name)
                    leaveChat(name)
                    """
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

def menu():
     message = '\n\n***********_MENU_*********\nType "/help" to see menu\nType "/kick (name)" to kick out\nType "/rooms" to see topic rooms\nType "/online" to see client online\nType "/private (name) (message)" to send private message\nTupe "/goRoom (room name)" to go ropic room\nType "/goPrivate (username)" to go private room with friend\nLeave chat by pressing ctrl + C\n***************************'
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

def kick_user(sender, kick):
    if(sender != kick):
        #If user in nicnames then kick out from room
        if  kick in nicknames:
            name_index = nicknames.index(kick)
            nicknames.remove(kick)
            
            client_to_kick = clients[name_index]
            clients.remove(client_to_kick)
            broadcast(f'{kick} was kicked out'.encode('ascii'))
            client_to_kick.send("You were kicked out".encode('ascii'))
            client_to_kick.close()
        else:
            name_index = nicknames.index(sender)        
            client_to_send = clients[name_index]
            client_to_send.send(f"No user named {kick} in online".encode('ascii'))
    else:
        name_index = nicknames.index(sender)        
        client_to_send = clients[name_index]
        client_to_send.send(f"You can't kick yourself out. To left chat room press CTRL + C".encode('ascii'))
        
"""def findClient(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client= clients[name_index]
        return client"""
    
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
    if sender != recipient:
        if recipient in nicknames:
            name_index = nicknames.index(recipient)        
            client_to_send = clients[name_index]
            client_to_send.send(f"{sender} (Private): {msg}".encode('ascii'))
        else:
            name_index = nicknames.index(sender)        
            client_to_send = clients[name_index]
            client_to_send.send(f"No user named {recipient} in online".encode('ascii'))
    else:
        name_index = nicknames.index(sender)        
        client_to_send = clients[name_index]
        client_to_send.send("You can't send yourself private message".encode('ascii'))

#Go Topic room
def goRoom(sender, room):
    if room in rooms:
        name_index = nicknames.index(sender)        
        client_to_go = clients[name_index]
        client_to_go.send(f"{sender} suppose to go room: {room}".encode('ascii'))
    else:
        name_index = nicknames.index(sender)        
        client_to_go = clients[name_index]
        client_to_go.send(f"No room named {room}".encode('ascii'))

#Go private room
def goPrivate(sender, buddy):
    if(buddy != sender):
        if buddy in nicknames:
            name_index_sender = nicknames.index(sender)        
            client_to_go_sender = clients[name_index_sender]
            client_to_go_sender.send(f"{sender} suppose to go private room with: {buddy}".encode('ascii'))

            name_index_buddy = nicknames.index(buddy)        
            client_to_go_buddy = clients[name_index_buddy]
            client_to_go_buddy.send(f"{buddy} suppose to go private room with: {sender}".encode('ascii'))
        else:
            name_index_sneder = nicknames.index(sender)        
            client_to_error = clients[name_index_sneder]
            client_to_error.send(f"No client named {buddy} in online".encode('ascii'))
    else: 
        name_index_sneder = nicknames.index(sender)        
        client_to_error = clients[name_index_sneder]
        client_to_error.send("You can't go private room alone".encode('ascii'))

#Leave from chat
"""def leaveChat(name):
    print('Hello')

    name_index = nicknames.index(name)
    nicknames.remove(name)
    client_to_leave = clients[name_index]
    clients.remove(client_to_leave)
    broadcast(f'{name} left the chat'.encode('ascii'))
    client_to_leave.send("You left the chat".encode('ascii'))
    client_to_leave.close()
    """
    
    
    


print("Server is listening...")
receive()
