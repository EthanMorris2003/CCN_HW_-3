import socket
import time
from pynput.keyboard import Listener

def on_press(key, client_socket):
    try:
        if key.char == 'a':
            client_socket.send('a'.encode()) 
        elif key.char == 'd':
            client_socket.send('d'.encode()) 
        elif key.char == 's':
            client_socket.send('s'.encode()) 
        elif key.char == 'w':
            client_socket.send('w'.encode()) 
    except AttributeError:
        pass

def client_program():
    print("trying to connect to server")
    host = "127.0.0.1"  # Use localhost or 127.0.0.1 for local connection
    port = 5000  # socket server port number

    client_socket = socket.socket()  
    client_socket.connect((host, port))  

    print("waiting for keyboard input")
    with Listener(on_press=lambda key: on_press(key, client_socket)) as listener:
        listener.join()

    client_socket.close() 

if __name__ == '__main__':
    client_program()