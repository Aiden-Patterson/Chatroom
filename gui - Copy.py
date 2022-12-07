from tkinter import *
import socket
import select
import errno

root = Tk()
root.title("Messager")
root.resizable(0,0)
USERNAME = ""

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 5050
# Create a socket
try:

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to a given ip and port
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
except: # there is no server, make this client act as the server

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # SO_ - socket option
    # SOL_ - socket option level
    # Sets REUSEADDR (as a socket option) to 1 on socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind, so server informs operating system that it's going to use given IP and port
    # For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
    server_socket.bind((IP, PORT))

    # This makes server listen to new connections
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

            # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(message_header):
                return False

            # Convert header to int value
            message_length = int(message_header.decode('utf-8').strip())

            # Return an object of message header and message data
            return {'header': message_header, 'data': client_socket.recv(message_length)}

        except:

            # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
            # or just lost his connection
            # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
            # and that's also a cause when we receive an empty message
            return False

    while True:

        # Calls Unix select() system call or Windows select() WinSock call with three parameters:
        #   - rlist - sockets to be monitored for incoming data
        #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
        #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
        # Returns lists:
        #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
        #   - writing - sockets ready for data to be send thru them
        #   - errors  - sockets with some exceptions
        # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


        # Iterate over notified sockets
        for notified_socket in read_sockets:

            # If notified socket is a server socket - new connection, accept it
            if notified_socket == server_socket:

                # Accept new connection
                # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                # The other returned object is ip/port set
                client_socket, client_address = server_socket.accept()

                # Client should send his name right away, receive it
                user = receive_message(client_socket)

                # If False - client disconnected before he sent his name
                if user is False:
                    continue

                # Add accepted socket to select.select() list
                sockets_list.append(client_socket)

                # Also save username and username header
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
                        # We are reusing here message header sent by sender, and saved username header send by user when he connected
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        # It's not really necessary to have this, but will handle some socket exceptions just in case
        for notified_socket in exception_sockets:

            # Remove from list for socket.socket()
            sockets_list.remove(notified_socket)

            # Remove from our list of users
            del clients[notified_socket]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to a given ip and port
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)













# send the message to the server
def sendMessage(message):
    send = message.encode('utf-8')
    message_header = f"{len(send):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + send)

# used to display the messages you send and the ones you recieve
def displayMessage(message):
    msgDisplay.insert(END, message)

#get the message from the textbox when you click the button, display it to the user and send it to the server
def myClick():
    if(textBox.get() != ''):
        global USERNAME
        # if username is empty, that means this is the first message of the program and put it as the USERNAME
        if USERNAME == "":
            USERNAME = textBox.get()
            textBox.delete(0, 'end')
            sendUser()
        else:
            displayMessage(USERNAME + ": " + textBox.get() +"\n")
            sendMessage(textBox.get() + "\n")
            textBox.delete(0, 'end')


#Build the GUI
scroller = Scrollbar(root)
myButton = Button(root, text="Send message", padx=15, pady = 15, command=myClick, fg="white", bg="blue")
msgDisplay = Listbox(root, width = 15, height = 15, yscrollcommand=scroller.set)
textBox = Entry(root, width=50, border=5)
scroller.config(command=msgDisplay.yview)

myButton.pack(side = BOTTOM)
scroller.pack(side = LEFT, fill = Y)
msgDisplay.pack(side=TOP, fill=X)
textBox.pack(side = BOTTOM)

#first message will always ask for the username, program will not connect to the server until an inital message is typed
displayMessage("Please enter your username")

# listen for any messages recieved
def getMessage():
    try:
        # loop over received messages and display them
        while True:
            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection
            if not len(username_header):
                displayMessage('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Receive and decode message
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            displayMessage(username + ": " + message)

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            print("THis is where the error is")

    #keep checking for new messages
    root.after(1000, getMessage)

#send the username to the server, called at the beginning after the initial message
def sendUser():
    my_user = USERNAME.encode('utf-8')
    username_header = f"{len(USERNAME):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + my_user)

    displayMessage( USERNAME + " has entered the chat. Say hello!")
    sendMessage("Has entered the chat. Say hello!")
    getMessage()

root.mainloop()
