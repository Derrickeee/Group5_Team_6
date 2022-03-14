import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import pandas as pd


console = Tk()
varOption = IntVar()

def run():
    tweets = entry_nooftweets.get()
    if not tweets:
        tkinter.messagebox.showerror(title="Empty Field!", message="Please enter number of tweets.", font="lucida 15")
    if tweets and not tweets.isnumeric():
        tkinter.messagebox.showerror(title="Empty Field!", message="Please enter an integer.")

def fileBrowser():
    """This function will only run after user presses browse-a-file button"""
    global file_path
    def hideFrames():
        """This function is used to clear all the contents in the frame after navigating to a new function"""
        contentFrame.pack_forget()  # forgets the frame storing content temporarily until it is being packed again.
        for widget in contentFrame.winfo_children():  # loops through all the widgets used in the content frame and destroy all of them
            widget.destroy()

        mainMenuFrame.pack_forget()  # forgets the mainMenuFrame which is different from the frame storing content.
        for widget in mainMenuFrame.winfo_children():
            widget.destroy()

        return

    MainPageLabel1.destroy()  # From this point on, the gui is remodelling itself by destroying past created labels and buttons
    MainPageLabel2.destroy()
    browseButton.destroy()

    # stores the file path of the user selected data-set to be used with our other functions
    file_path = filedialog.askopenfilename(initialdir="",
                                           title="Select Dataset File",
                                           filetypes=((".csv Files", "*.csv"), ("All Files", "*.*")))

    file_name = file_path  # In same Folder
    file = pd.read_csv(file_name, sep=",")  # Opens CSV in same folder as the .py file
    df = pd.DataFrame(file)  # Converts to dataframe for easier handling

    # Window that updates after selecting CSV file
    console.geometry("1000x650")


# Create Label to instruct users to browse for data
MainPageLabel1 = Label(console, text="Welcome to our program!")
MainPageLabel2 = Label(console, text="Click on the button above to browse for a Dataset!")
# Button to browse for Dataset
browseButton = Button(console, text="Browse", padx=30, pady=10, command=fileBrowser)
mainMenuFrame = Frame(console, relief=SUNKEN, height=800, width=1000, background='Black')
buttonFrame = Frame(console, height=100, width=1000, borderwidth=10, relief=GROOVE, background='Black')
mainframe = Frame(console, height=550, width=1000, borderwidth=10, relief=SUNKEN, background='Black')
contentFrame = Frame(mainframe, height=600, width=1000, borderwidth=10)

"""def listbox_used(event):
    print(listbox.get(listbox.curselection()))


listbox = tkinter.Listbox(height=4)
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()"""


def fileBrowserFromMenu():  # will run if user selects the option to reupload dataset from the menu page
    """This function runs if user selects the option to reupload dataset from the menu page"""
    fileBrowser()  # prompts user to select file again
    mainMenuFrame.pack_forget()  # removes the mainmenuframe

if __name__== "__main__":
    console.title("Obfuscation Algorithm")
    console.geometry("900x600")
    entry_nooftweets = Entry(console, font="lucida 23 bold", width=20)
    title = Label(console, text="Obfuscate", fg="blue", font="lucida 25 bold").place(
        x=150, y=220)

    submit_button = Button(console, text="Diffname", bg="red3", font="lucida 15 bold", borderwidth=3, height=1,
                           width=8).place(x=700, y=340)
    submit_button2 = Button(console, text="Download APK", bg="red3", font="lucida 15 bold", borderwidth=3, height=1,
                            width=13).place(x=700, y=390)
    submit_button3 = Button(console, text="Rebuild APK", bg="red3", font="lucida 15 bold", borderwidth=3, height=1,
                            width=13).place(x=700, y=440)
    submit_button4 = Button(console, text="Browse", bg="red3", font="lucida 15 bold", borderwidth=3, height=1,
                            width=13, command=fileBrowserFromMenu).place(x=700, y=150)
    entry_nooftweets.place(x=250, y=140)
    sentiment = Label(console)
    sentiment.pack()
    console.mainloop()