# Overview

This is a simple chatroom application made in Python. A server is run, and multiple clients are able to connect to that server and communicate with each other.

I wanted practice in Python, as well as useful practice in getting computers to communicate with each other. Right now the clients work only over localhost, but it can be easily changed by changing what IP address the client looks for.

[Software Demo Video](http://youtube.link.goes.here)

# Network Communication

I used a client/server architecture for this build, so that I could have multiple clients all communicating with each other.
I used UDP on port 5050. I used this port because I did research and found it as a port that is usually open and not used for many things.
I encoded messages with UTF-8 since it is the most commonly used encoding and easiest to use.

# Development Environment

I used Python to run the chatroom. I used Tkinter to create a user interface that also allowed for a much more refined chatroom. In the tutorial I followed, they ade the chatroom in the command line, and it would only update the recieved messages once a message was sent. Using Tkinter, I created an interface that is constantly looking for received messages, as well as able to send a message at any time.

# Useful Websites

* [Socket and chatroom tutorial](https://pythonprogramming.net/sockets-tutorial-python-3/)
* [Tkinter reference](https://www.tutorialspoint.com/python/python_gui_programming.htm)
* [Python socket reference](https://docs.python.org/3/howto/sockets.html)

# Future Work

* Allow for the chosen username to be saved so that the user doesn't have to input it every time. Add another way to change the username during execution
* Save messages that are sent while only one person is connected to the server, then send them all when someone new connects
