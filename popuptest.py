#Import the required Libraries
from tkinter import *
from tkinter import ttk
#Create an instance of Tkinter frame
win = Tk()
#Set the geometry of Tkinter frame
win.geometry("750x270")

def open_popup():
   top= Toplevel(win)
   top.geometry("750x250")
   top.title("Child Window")
   Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)

Label(win, text=" Click the Below Button to Open the Popup Window", font=('Helvetica 14 bold')).pack(pady=20)
#Create a button in the main Window to open the popup
ttk.Button(win, text= "Open", command= open_popup).pack()
win.mainloop()