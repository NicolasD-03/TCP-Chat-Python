import os
import socket
import sys
import threading
from time import sleep

# Const variables
if len(sys.argv) == 3:
    HOST: str = str(sys.argv[1])
    PORT: int = int(sys.argv[2])
else:
    HOST: str = "127.0.0.1"
    PORT: int = 6666


# Starting server and (creating and bind the socket)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("----- SERVER IS STARTED -----")

# List of connected clients
clients = []
# List of connected clients nicknames
nicknames = []


def broadcast(message: str):
    """Send message to all connected clients

    Parameters
    ----------
    message : str
        The message to send
    """
    # Send message for each client in connected clients list
    for client in clients:
        client.send(message)


def handle(client: socket):
    """Waiting for a message from a client and send it to all connected client

    Parameters
    ----------
    client : socket
        The client socket
    """
    # Infinite loop (New thread for each client)
    while True:
        try:
            # Waiting a message
            message = client.recv(1024)
            # Sending it to all connected client
            if message != "PING":
                broadcast(message)
        except:
            break


def receive():
    """Main function waiting for client connection, get info like nickname and create thread of handle()"""
    while True:
        # Accept client connection
        client, address = server.accept()
        # Print in the server console address of the client
        print(f"Connected with {str(address)}")

        # Ask to client his nickname
        client.send("NICK".encode("utf8"))
        # Get the nickname
        nickname = client.recv(1024).decode("utf8")
        # Adding nickname to the list of the connected clients nicknames
        nicknames.append(nickname)
        # Adding client to the list of the connected clients
        clients.append(client)

        # Print in the server console the client nickname
        print(f"Client name is {nickname}")
        # Send to all connected clients the info about the new connected client
        broadcast(f"SERVER >> {nickname} joined the chat".encode("utf8"))
        # Send to the client a welcome message
        client.send("\nYou are connected !".encode("utf8"))

        # Create a thread for handle() to wait message from this client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def ping(ping_every: int):
    """Just ping each client with a message to see if it is connected

    Parameters
    ----------
    ping_every : int
        Time between each ping
    """
    while True:
        # Wait for each ping
        sleep(ping_every)
        # For each client send "PING" to see if it respond
        for client in clients:
            try:
                client.send("PING".encode("utf8"))
            # If client doesn't respond it is removed
            except:
                # Find client index
                index = clients.index(client)
                # Remove client from connected clients list
                clients.remove(client)
                # Close the connection with the client
                client.close()
                # Get the nickname of the client with his index
                nickname = nicknames[index]
                # Send to all client a message about the deconnection
                broadcast(
                    f"SERVER >> {nickname} left the chat !".encode("utf8")
                )
                # Remove client nickname from the connected clients nicknames list
                nicknames.remove(nickname)


def command():
    """Command function to process some command server side only"""
    while True:
        # Wait for a command
        command = input("")
        if command == "/help":
            print("----- HELP -----")
            print("/help - Show this help")
            print("/list - Show connected clients nicknames list")
            print("/kick <client_nickname> - Kick a client")
            print("/stop - Stop the server")
            print("-----------------")
        # If command == list, show connected clients nicknames list
        elif command == "/list":
            print(nicknames)
        # If command == kick, kick the client
        elif command.split()[0] == "/kick":
            # Verify if nickname is in the connected clients nicknames list
            if len(command.split()) > 1 and command.split()[1] in nicknames:
                # Get the index of nickname
                index = nicknames.index(command.split()[1])
                # Get the client with the nickname index
                client = clients[index]
                # Send to the client a message to inform him that he is kicked
                client.send("KICKED".encode("utf8"))
                # Remove client nickname from the connected clients nicknames list
                nicknames.remove(command.split()[1])
                # Remove client from connected clients list
                clients.remove(client)
                # Close the connection with the client
                client.close()
                # Send to all client a message about the kicked
                broadcast(
                    f"SERVER >> {command.split()[1]} has been kicked of the chat !".encode(
                        "utf8"
                    )
                )
            else:
                print("User doesn't exist")
        # If command == stop, close the server
        elif command == "/stop":
            server.close
            os._exit(0)
        else:
            print("INVALID COMMAND")


if __name__ == "__main__":

    # Create a thread for ping()
    thread_ping = threading.Thread(target=ping, args=(1,))
    thread_ping.start()

    # Create a thread for command()
    thread_command = threading.Thread(target=command)
    thread_command.start()

    # Execute main function to wait client connection
    receive()
