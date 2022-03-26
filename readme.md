# Simple TCP chat server-client

## Description

A simple TCP chat server-client application in python. The server listens on a port and accepts connections. When a client connects, the server sends a welcome message and waits for the client to send a message. The server then sends the message to all connected clients.

## Features

- Server and client can be run on the same or on different machine

- Server command are available :

  - `/help` : display the list of available commands
  - `/stop` : close the server
  - `/list` : display the list of connected clients
  - `/kick <client_nickname>` : kick a client

- Client command are available :

  - `/help` : display the list of available commands
  - `/quit` : close the client

- Allow multiple client to connect to the server

- Multithreaded server and client

## Setup

### Docker

Just type this to your terminal with docker installed, you can bind the host port to `6666` _ex : -p <desired_host_port>:6666_

    $docker run -dit nicolasd57/tcp-chat-python

You need `python 3.6` or later to run this application. _(Not tested on python version above 3.6)_\
Clone the repo on your device and go and open the folder

### Server

    $python server.py <IP_Adress> <PORT>
    or
    $python3 server.py <IP_Adress> <PORT>

### CLient

    $python client.py <IP_Adress> <PORT>
    or
    $python3 client.py <IP_Adress> <PORT>
