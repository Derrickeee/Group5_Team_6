import tkinter.messagebox
from tkinter import *
from tkinter import filedialog, messagebox
import pandas as pd
from werkzeug.utils import secure_filename
import time
import os

import javaobfuscator
import apkobfuscator

console = Tk()


def fileBrowser():
    global tf
    global file_name
    global file_path
    tf = filedialog.askopenfilename(
        initialdir="",
        title="Open Text file",
        filetypes=(("SMALI Files", "*.smali"),("APK Files", "*.apk"),("JAVA Files", "*.java"),("Kotlin Files","*.kt"))
    )
    file_name = os.path.basename(tf)
    file_path = tf
    entry.insert(END, tf)



def find_files(file_name, search_path):
   result = []

   for root, dir, files in os.walk(search_path):
      if file_name in files:
         result.append(os.path.join(root, file_name))
         print(search_path)
   return result


def proceed():
    # will run if user selects the option to reupload dataset from the menu page


    tfi = open(tf, 'r')
    data = tfi.read()
    mainMenuFrame.pack_forget()
    my_frame1.pack()
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
    if tf[-4:].lower() in ['java']:
        javaFile = tf
        javaobfuscator.main(javaFile, 'obfuscated_' + file_name)

        # Grab obfuscated file contents for output
        with open('obfuscated_' + file_name, 'r', encoding='utf-8-sig') as file:
            obfuscatedContents = file.read()
            file.close()
            txt2.insert(END, obfuscatedContents)
    elif tf[-3:].lower() in ['apk']:
        filepath = tf
        name, folder, fileList = apkobfuscator.getFileName(filepath)
        path = None
        for file in fileList:
                path = os.path.abspath(file)  # Get the file path
                fileOb, obfuscatedText = apkobfuscator.main_obfuscation(path)
                txt2.insert(END, fileOb)

               # Rename the class files
        apkobfuscator.class_rename(folder)

               # Pack the folder back into apk
        apkobfuscator.packing(name)
            # Delete the working path
            # path = os.getcwd() + "\\"+folder
            # shutil.rmtree(path)

        #rawFilename = javaFile.split('/')[-1]
        # Obfuscate the java file uploaded
        #start = time.time()

        #with open(rawFilename, 'r', encoding='utf-8-sig') as file:
            #obfuscatedContents = file.read()
            #txt2.insert(END, obfuscatedContents)
            #file.close()
    # start = time.time()
    # originalSize = os.stat(data).st_size
    # end = time.time()
    # obfuscatedSize = os.stat(data).st_size
    # # Calculate size difference of the two MainActivity.smali in percentage
    # sizeDiff = (obfuscatedSize / originalSize) * 100
    # if sizeDiff > 0:
    #     sizePercentage = '+' + str(round(sizeDiff, 2)) + '%'
    #
    # else:
    #     sizePercentage = '-' + str(round(sizeDiff, 2)) + '%'
    #
    # tf.close()


        """This function runs if user selects the option to reupload dataset from the menu page"""
  # prompts user to select file again
    # removes the mainmenuframe
    # Window that updates after selecting CSV file
console.geometry("1000x650")






# Create Label to instruct users to browse for data

# Button to browse for Dataset

mainMenuFrame = Frame(console, relief=SUNKEN, height=800, width=1000, background='orange')
buttonFrame = Frame(console, height=100, width=1000, borderwidth=10, relief=GROOVE, background='green')
mainframe = Frame(console, height=550, width=1000, borderwidth=10, relief=SUNKEN, background='orange')
my_frame1 = Frame(console, height=800, width=1000, borderwidth=10, background='orange')
contentFrame = Frame(mainframe, height=600, width=1000, borderwidth=10)




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
    console.mainloop()