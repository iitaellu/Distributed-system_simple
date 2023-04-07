import threading
import socket

# Choosing Nickname
nickname = input("choose a nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 3000))

stop_thread = False

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
             # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode('ascii'))
                pass
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = f'{nickname}: {input("")}' 
        """if (message[len(nickname)+2:] == "quit"):
            client.send(f'LEAVE {nickname}'.encode('ascii'))"""
        if (message[len(nickname)+2:].startswith('/')):
            if message[len(nickname)+2:].startswith('/kick'):
                client.send(f'KICK {nickname} {message[len(nickname)+2+6:]}'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/rooms'):
                client.send(f'ROOMS {nickname}'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/online'):
                client.send(f'ONLINE {nickname}'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/help'):
                client.send(f'HELP {nickname}'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/private'):
                client.send(f'PRIVATE {nickname} {message[len(nickname)+2+9:]}'.encode('ascii'))
            """          
            elif message[len(nickname)+2:].startswith('/leave'):
                client.send(f'LEAVE {nickname}'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/goRoom'):
                client.send(f'GOROOM {roomname}{message[len(nickname)+2+6:]}'.encode('ascii'))
            elif message[len(nickname)+2:].startswith('/goPrivate'):
                client.send(f'GOPRIVATE {message[len(nickname)+2+6:]}'.encode('ascii'))
            """
        else:
            client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
