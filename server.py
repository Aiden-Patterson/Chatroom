import socket
import select

HEADER_LENGTH = 10

IP = "0.0.0.0"
PORT = 5050

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
server_socket.bind((IP, PORT))

# listen to new connections
server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving
def receive_message(client_socket):

    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:

            # Accept new connection
            client_socket, client_address = server_socket.accept()

            # first message from a new client is their username
            user = receive_message(client_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                continue

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # save username and username header
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        # Else existing socket is sending a message
        else:

            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:

                    # Send user and message (both with their headers)
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    #handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]

