import threading
import socket

host = '127.0.0.1'
port = 3000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
#rooms = ['JavaScript', 'C/C#', 'Python']

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            print(msg)
            print(nicknames)
            if msg.decode('ascii').startswith('KICK'):
                name_to_kick = msg.decode('ascii')[5:]
                print("Hello")
                kick_user(name_to_kick)
            else:
                broadcast(message)
            """if msg.decode('ascii').startswith('ROOMS'):
                print(rooms)
                name = msg.decode('ascii')[6:]
                printList(name)"""
             
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break
            """elif msg.decode('ascii').startswith('LEAVE'):
                name_to_leave = msg.decode('ascii'[6:])
                leave(name_to_leave)
                break
            elif msg.decode('ascii').startswith('PRIVATE'):
                name_to_private = msg.decode('ascii'[8:])
                pass
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
       

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of clients is {nickname}!")
        broadcast(f'{nickname} joined to chat!'.encode('ascii'))

        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    print(name)
    
    if name in nicknames:
        print("HELlo Again")
        name_index = nicknames.index(name)
        nicknames.remove(name)
        
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        broadcast(f'{name} was kicked out'.encode('ascii'))
        client_to_kick.send("You were kicked out".encode('ascii'))
        client_to_kick.close()
        
        

#def printList(name):
 #   print(name)
  #  print(nicknames)
   # print("hello")
    #name_index = nicknames.index(name)
    #client_for_show = clients[name_index]
    #name_index2 = nicknames.index(name)
    #print(name_index2)
    #client_for_show = clients[name_index2]
    #client_for_show.send("THE ROOMS").encode('ascii')

def leave(name):
    name_index = nicknames.index(name)
    client_to_leave = clients[name_index]
    clients.remove(client_to_leave)
    client_to_leave.send("You left the chat")
    client_to_leave.close()
    nicknames.remove(name)
    broadcast(f'{name} left the chat' )


print("Server is listening...")
receive()

"""from xmlrpc.server import SimpleXMLRPCServer
import datetime
import xml.etree.ElementTree as ET

import socket
import sys
import time

users = []

def addUser(userName, IP):
    user = [userName, IP]
    users.append(user)
    return '\n--------------------------------\n User named :'+userName+' added\n--------------------------------\n\n'

def print_users():   
    return users

def bindHost(userName):
    
    new_socket = socket.socket()
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    port = 8080
    new_socket.bind((host_name, port))
    print("Binding successful")
    addUser(userName, ip)
    new_socket.listen(1)
    return "Your IP: " + ip
    

server = SimpleXMLRPCServer(("localhost", 3000))
print("Listening on port 3000...")
server.register_function(addUser, "addUser")
server.register_function(print_users, "print_users")
server.register_function(bindHost, "bindHost")
server.serve_forever()
"""


"""
import socket
import sys
import time

new_socket = socket.socket()
host_name = socket.gethostname()
s_ip = socket.gethostbyname(host_name)
port = 8080

new_socket.bind((host_name, port))
print("Binding successful!")
print("This is your IP: ", s_ip)

name = input('Enter name:')
new_socket.listen(1)

conn, add= new_socket.accept()
print("Received connection from ", add[0])
print('Connection Established. Connected From: ',add[0])

client = (conn.recv(1024)).decode()
print(client + ' has connected.')
conn.send(name.encode())

while True:
    message = input('Me : ')
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    print(client, ':', message)
"""

"""
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 3000

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    client, address = server.accept()
    print("Connected with {}".format(str(address)))
    while True:
        # Accept Connection
        

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()"""
