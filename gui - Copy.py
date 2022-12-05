from tkinter import *
import socket
import select
import errno

root = Tk()
root.title("Messager")
root.resizable(0,0)
username = "Tommy"

HEADER_LENGTH = 10
IP = "10.50.125.73"
PORT = 1234

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

client_socket.setblocking(False)

#send the username to the server
my_user = username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + my_user)

# listen for any messages recieved
def getMessage():
    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:
            #msgDisplay.insert(END, "This is the while True loop in getMessage")
            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            displayMessage(message)

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

    #keep checking for new messages
    root.after(1000, getMessage)

# send the message to the server
def sendMessage(user, message):
    send = user + ": " + message
    send = send.encode('utf-8')
    message_header = f"{len(send):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + send)

# used to display the messages you send and the ones you recieve
def displayMessage(message):
    msgDisplay.insert(END, message)

#send the message when you click the send button
def myClick():
    if(textBox.get() != ''):
        displayMessage(username + ": " + textBox.get() +"\n")
        sendMessage(username, textBox.get() + "\n")
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
displayMessage( username + " has entered the chat. Say hello!")
sendMessage(username, "Has entered the chat. Say hello!")
getMessage()
root.mainloop()
