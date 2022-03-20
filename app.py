import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import pandas as pd


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

    tf.close()

#df = pd.DataFrame(file)  # Converts to dataframe for easier handling

    # Window that updates after selecting CSV file
console.geometry("1000x650")


# Create Label to instruct users to browse for data

# Button to browse for Dataset

mainMenuFrame = Frame(console, relief=SUNKEN, height=800, width=1000, background='orange')
buttonFrame = Frame(console, height=100, width=1000, borderwidth=10, relief=GROOVE, background='green')
mainframe = Frame(console, height=550, width=1000, borderwidth=10, relief=SUNKEN, background='orange')

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
    mainMenuFrame.pack_forget()


if __name__== "__main__":
    console.title("Obfuscation Algorithm")
    console.geometry("900x1200")
    entry = Entry(mainMenuFrame, font="lucida 23 bold", width=20)
  #  title = Label(mainMenuFrame, text="Obfuscate", fg="blue", font="lucida 25 bold").place(
       # x=150, y=350)
    mainMenuFrame.pack()
    continue_button = Button(mainMenuFrame, text="Continue", bg="red3", font="lucida 15 bold", borderwidth=3, height=1,
                           width=8, command=proceed).place(x=700, y=340)
    browseButton = Button(mainMenuFrame, text="Browse", bg="red3", font="lucida 15 bold", borderwidth=3, height=1,
                            width=13, command=fileBrowser).place(x=700, y=50)


    entry.place(x=250, y=140)
    sentiment = Label(console)
    sentiment.pack()
    console.mainloop()