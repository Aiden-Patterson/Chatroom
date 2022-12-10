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
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

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
