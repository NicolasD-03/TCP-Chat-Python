import os
import socket
import threading
import sys
from time import sleep

# Const variables
HOST: str = str(sys.argv[1]) or "127.0.0.1"
PORT: int = int(sys.argv[2]) or 6666

# Ask a nickname
nickname = input("Enter your nickname for the chat : ")

# Create a socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive():
    """Main function to wait message from the server"""
    while True:
        try:
            message = client.recv(1024).decode("utf8")

            # If message == NICK, send the nickname to the server
            if message == "NICK":
                client.send(nickname.encode("utf8"))
            # If message == KICKED, print a message, close the connection and exit
            if message == "KICKED":
                print("SERVER >> You have been kicked")
                client.close()
                os._exit(0)
            # If message != PING show the message
            elif message != "PING":
                print(message)
        except:
            break


def write():
    """Function to get a message and send it to the server"""
    while True:
        try:
            # Wait for a message
            inputMessage = input("")
            if inputMessage == "QUIT":
                # Close the connection and quit
                client.close()
                os._exit(0)
            else:
                # Adding nickname to the inputMessage
                message = f"{nickname} >> {inputMessage}"
                # Send the message to the server
                client.send(message.encode("utf8"))
        except:
            break


def ping(ping_every: int):
    """Ping the server to see if the server is up

    Parameters
    ----------
    ping_every : int
        Time between each ping
    """
    while True:
        sleep(ping_every)
        try:
            # Send PING message to the server
            client.sendall("PING".encode("utf8"))
        except:
            # If the message can't reach show a message close the connection and quit
            print("Sorry your message can't be delliver, server is ofline")
            client.close()
            os._exit(0)


if __name__ == "__main__":
    # Create a thread for receive()
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # Create a thread for write()
    write_thread = threading.Thread(target=write)
    write_thread.start()

    # Create a thread for ping()
    receive_ping = threading.Thread(target=ping, args=(1,))
    receive_ping.start()
