import tkinter.messagebox
from tkinter import *

interface = Tk()
varOption = IntVar()

def run():
    tweets = entry_nooftweets.get()
    if not tweets:
        tkinter.messagebox.showerror(title="Empty Field!", message="Please enter number of tweets.", font="lucida 15")
    if tweets and not tweets.isnumeric():
        tkinter.messagebox.showerror(title="Empty Field!", message="Please enter an integer.")

def do():
    if varOption.get() == 1:
        sentiment.config(text="Positive")
    else:
        sentiment.config(text="Negative")

"""def listbox_used(event):
    print(listbox.get(listbox.curselection()))


listbox = tkinter.Listbox(height=4)
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()"""

if __name__== "__main__":
    interface.title("Obfuscation Algorithm")
    interface.geometry("900x600")
    title = Label(interface, text="Obfuscate", fg="blue", font="lucida 25 bold").place(
        x=150, y=80)
    rb_pos = Radiobutton(interface, text = "Positive", font="lucida 25 bold", variable = varOption, value = 1).place(x=250, y=150)
    rb_neg = Radiobutton(interface, text="Negative", font="lucida 25 bold", variable=varOption, value=2).place(x=250,y=200)
    entry_nooftweets = Entry(interface, font="lucida 23 bold", width=10)
    submit_button = Button(interface, text="Submit", bg="red3", font="lucida 15 bold", borderwidth=3, command=lambda:[do(), run()], height=1,
                           width=8).place(x=435, y=340)
    entry_nooftweets.place(x=250, y=270)
    sentiment = Label(interface)
    sentiment.pack()
    interface.mainloop()