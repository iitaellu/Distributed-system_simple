import threading
import socket

nickname = input("choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 3000))

stop_thread = False

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode('ascii'))
                pass
            else:
                print(message)
        except:
            print("An error occured")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}' 
        """if (message[len(nickname)+2:] == "quit"):
            client.send(f'LEAVE {nickname}'.encode('ascii'))"""
        if (message[len(nickname)+2:].startswith('/')):
            if message[len(nickname)+2:].startswith('/kick'):
                client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/rooms'):
                client.send(f'ROOMS {nickname}{message[len(nickname)+2+6:]}'.encode('ascii'))
            """elif message[len(nickname)+2:].startswith('/private'):
                client.send(f'PRIVATE {message[len(nickname)+2+6:]}'.encode('ascii'))"""
        else:
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


"""
import xmlrpc.client
import xml.etree.ElementTree as ET
import socket
import sys
import time

def main():

    socket_server = socket.socket()
    server_host = socket.gethostname()
    ip = socket.gethostbyname(server_host)
    port = 8080
    
    socket_server.bind((server_host, port))
    print("Binding successful!")
    print("This is your IP: ", ip)
    socket_server.listen(1) 
    

    proxy = xmlrpc.client.ServerProxy("http://localhost:3000/")
    username = input("set Nickname: ")
    msg = proxy.addUser(username, ip)
    print(msg)
    #msg = proxy.bindHost(username)
    #print(msg)
    
    #print(f"{result}")
    
    userInput = -1
    while(userInput != "0"):
        print("\nMenu options:")
        print("1: Enter private discussion")
        print("2: Enter Room")
        print("3. Print user which are online")
        print("0: Quit")
        userInput = input("What do you want to do? ")
        if userInput == "1":
            #msg = proxy.bindHost()
            #print(msg)
            server_host = input('Enter friend\'s IP address:')
            name = input('Enter Friend\'s name: ')
            socket_server.connect((server_host, port))
            socket_server.send(name.encode())
            server_name = socket_server.recv(1024)
            server_name = server_name.decode()
            
            #result = proxy.addUser(username, ip)
            #print(f"{result}")
        if userInput == "2":
            
            server_host = input('Enter friend\'s IP address:')
            name = input('Enter Friend\'s name: ')
            #message = proxy.print_all()
            #print(message)
        if userInput == "3":
            users = proxy.print_users()
            for user in users:
                print("Username: "+user[0]+", IP: "+user[1])   
        if userInput == "0":
            print("Ending software...")

    

main()
"""
"""
import socket
import sys
import time

socket_server = socket.socket()
server_host = socket.gethostname()
ip = socket.gethostbyname(server_host)
sport = 8080

print('This is your IP address: ', ip)
server_host = input('Enter friend\'s IP address:')
name = input('Enter Friend\'s name: ')
 
socket_server.connect((server_host, sport))

socket_server.send(name.encode())
server_name = socket_server.recv(1024)
server_name = server_name.decode()
 
print(server_name,' has joined...')
while True:
    message = (socket_server.recv(1024)).decode()
    print(server_name, ":", message)
    message = input("Me : ")
    socket_server.send(message.encode())  
"""

"""
import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 3000))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message != '':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
"""
