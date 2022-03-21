import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import pandas as pd
from werkzeug.utils import secure_filename
import time
import os

console = Tk()




def fileBrowser():
    tf = filedialog.askopenfilename(
        initialdir="",
        title="Open Text file",
        filetypes=(("Text Files", "*.txt"),("SMALI Files", "*.smali"),("APK Files", "*.apk"),("JAVA Files", "*.java"),("Kotlin Files","*.kt"))
    )
    entry.insert(END, tf)
    tf = open(tf, 'r')
    data = tf.read()
    mainMenuFrame.pack_forget()
    my_frame1.pack()

    def mutliple_yview(*args):
        txt1.yview(*args)
        txt2.yview(*args)

    def mutliple_xview(*args):
        txt1.xview(*args)
        txt2.xview(*args)
    hor_scroll = Scrollbar(my_frame1, orient='horizontal')
    hor_scroll.pack(side=BOTTOM, fill=X)
    text_scroll = Scrollbar(my_frame1)
    text_scroll.pack(side=RIGHT, fill=Y)
    txt1 = Text(my_frame1, width=100, height=15, yscrollcommand=text_scroll.set
                , wrap="none", xscrollcommand=hor_scroll.set)
    txt1.pack(pady=0)
    # SECOND textbox
    txt2 = Text(my_frame1, width=100, height=15, yscrollcommand=text_scroll.set
                , wrap="none", xscrollcommand=hor_scroll.set)
    txt2.pack(pady=10)
    text_scroll.config(command=mutliple_yview)
    hor_scroll.config(command=mutliple_xview)

    txt1.insert(END, data)
    start = time.time()
    originalSize = os.stat(data).st_size
    end = time.time()
    obfuscatedSize = os.stat(data).st_size
    # Calculate size difference of the two MainActivity.smali in percentage
    sizeDiff = (obfuscatedSize / originalSize) * 100
    if sizeDiff > 0:
        sizePercentage = '+' + str(round(sizeDiff, 2)) + '%'

    else:
        sizePercentage = '-' + str(round(sizeDiff, 2)) + '%'


    tf.close()

#df = pd.DataFrame(file)  # Converts to dataframe for easier handling

    # Window that updates after selecting CSV file
console.geometry("1000x650")


# Create Label to instruct users to browse for data

# Button to browse for Dataset

mainMenuFrame = Frame(console, relief=SUNKEN, height=800, width=1000, background='orange')
buttonFrame = Frame(console, height=100, width=1000, borderwidth=10, relief=GROOVE, background='green')
mainframe = Frame(console, height=550, width=1000, borderwidth=10, relief=SUNKEN, background='orange')
my_frame1 = Frame(console, height=800, width=1000, borderwidth=10, background='orange')
contentFrame = Frame(mainframe, height=600, width=1000, borderwidth=10)

"""def listbox_used(event):
    print(listbox.get(listbox.curselection()))


listbox = tkinter.Listbox(height=4)
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()"""


def proceed():  # will run if user selects the option to reupload dataset from the menu page
    """This function runs if user selects the option to reupload dataset from the menu page"""
  # prompts user to select file again
    # removes the mainmenuframe



if __name__== "__main__":
    console.title("Obfuscation Algorithm")
    console.geometry("900x1200")
    entry = Entry(mainMenuFrame, font="lucida 23 bold", width=20)
  #  title = Label(mainMenuFrame, text="Obfuscate", fg="blue", font="lucida 25 bold").place(
       # x=150, y=350)
    mainMenuFrame.pack()
    continue_button = Button(mainMenuFrame, text="Continue", bg="red3", font="lucida 15 bold", borderwidth=3, height=1,
                           width=8, command=proceed).place(x=600, y=340)
    browseButton = Button(mainMenuFrame, text="Browse", bg="red3", font="lucida 15 bold", borderwidth=3, height=1,
                            width=13, command=fileBrowser).place(x=600, y=50)


    entry.place(x=100, y=50)
    sentiment = Label(console)
    sentiment.pack()
    console.mainloop()