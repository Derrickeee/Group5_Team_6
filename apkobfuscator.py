import random
import string
import re
import os

pswitch_string = []


# Trivial Obfuscation technique
def removeline(data):
    for i in range(len(data)):
        if data[i] != "\n" and data[i].__contains__(".line"):
            data[i] = "\n"


def nopsled(data):
    total = len(data)
    i = 0
    while (i < total):
        if data[i].__contains__(".method") or data[i].__contains__(".locals") or data[i].__contains__("cond") or data[
            i].__contains__("goto"):
            rand = random.randint(1, 100)
            for x in range(rand):
                data.insert(i + 1, "nop\n")
        total = len(data)
        i += 1


def insertjunk(data):
    replacement = []
    i = 0
    while i < len(data):
        if data[i].__contains__("Ljava/lang/System;->out:Ljava/io/PrintStream;"):
            replacement.append(data[i + 2].split(",")[0])
        i += 1

    total = len(data)
    i = 0
    stringList = generateStrJunk()
    while (i < total):
        if data[i].__contains__("Ljava/lang/System;->out:Ljava/io/PrintStream;"):
            for string in stringList:
                final_string = replacement[0] + ',' + string + '\n'
                data.insert(i + 2, final_string)
        total = len(data)
        i += 1
    nopsled(data)


# Important Obfuscation technique
def reorder(data):
    minLimit = 1
    maxLimit = 100
    label_start = ":goto__"
    label_end = "goto :goto__"  # Used similarly in the smali code
    database = []
    start_index = []
    end_index = []
    switch_var = []
    flag = None

    # Filter for .method and .end method
    for i in range(len(data)):
        if data[i].__contains__(".method"):
            start_index.append(i)
            flag = 1
        elif data[i].__contains__(".end annotation") and flag == 0:
            start_index.append(i)
            flag = 1
        elif (data[i].__contains__("return") or data[i].__contains__(".annotation")) and flag == 1:
            end_index.append(i)
            flag = 0
    randInt = random.randint(minLimit, maxLimit)
    database.append(randInt)
    for i in range(len(start_index)):  # Generate the gotos
        start = start_index[i]
        end = end_index[i]
        for x in range(start, end + 1):
            randInt = random.randint(minLimit, maxLimit)
            while randInt in database:  # Regenerate the randInt again
                minLimit = maxLimit
                maxLimit = maxLimit * 100
                randInt = random.randint(minLimit, maxLimit)
            segmentation = ":pswitch_" + str(randInt) + "\n"
            endofLabel = label_end + str(randInt) + "\n"
            startofLabel = label_start + str(database[-1]) + "\n"
            randStr = getRandstring(10)

            if data[x].__contains__(".method"):
                data[start] = data[start] + endofLabel
                database.append(randInt)
                flag = 1
            elif data[x].__contains__(".end annotation") and flag == 0:
                data[start] = data[start] + endofLabel
                database.append(randInt)
                flag = 1
            elif (data[x].__contains__("return") or data[x].__contains__(".annotation")) and flag == 1:
                data[end] = startofLabel + data[end]
                flag = 0
            # elif data[x].__contains__(".locals") and flag == 1: #For code Segmentation
            #     var_num = int(data[x].split(".locals")[1].strip("\n"))
            #     if var_num+1 <= 15:
            #         data[x] = ".locals "+ str(var_num+1)+"\n"
            #         var_declare="const/4 v" + str(var_num)+", "+"0x1\n"
            #         switch_declare="packed-switch v" + str(var_num)+", :" + "pswitch_data_"+randStr+"\n"
            #         data[x] = startofLabel + data[x]+var_declare + switch_declare + endofLabel
            #         switch_var.append(str(var_num))
            #         pswitch_string.append(randStr)
            #         database.append(randInt)
            #         seg_flag = 1
            elif (data[x] != "\n" or data[x] != "") and flag == 1:  # Included the pswitch label
                # endofLabel_goto = "goto :goto_switch"+"\n"
                # data[x] = segmentation+startofLabel + data[x]  + endofLabel_goto
                data[x] = segmentation + startofLabel + data[x] + endofLabel
                database.append(randInt)

    # #Data Reshuffling
    reshuffle(data, start_index, end_index)
    # Switch Segmentation
    # if seg_flag ==1:
    #     code_segmentation(data,switch_var)


def class_rename(path):
    fileList = []
    rename_dict = {}
    for root, sub, files in os.walk(path):
        for file in files:
            if ("\com\\" in root) and ("\google\\" not in root) and (file != "MainActivity.smali"):
                path = root + "\\" + file
                fileList.append(path)

    for file in fileList:

        # Get random name
        length = random.randint(8, 10)
        randString = getRandstring(length)

        # Get the name of the file
        name = file.split('\\')[-1].split(".smali")[0]
        rename_dict[name] = randString

        # Overwrite data
        fileread = open(file, "r")
        update = fileread.read()
        for key, value in rename_dict.items():
            update = update.replace(key, value)
            if update != "":
                filewrite = open(file, "w")
                filewrite.write(update)  # write obs class name
                filewrite.close()
        fileread.close()

        # Get the file path
        abspath = ''.join(os.path.abspath(file).split(name + ".smali"))
        newFilename = rename_dict.get(name) + '.smali'
        newabspath = abspath + newFilename
        os.rename(file, newabspath)  # rename file


def unreachable(data):
    size = len(data)
    i = 0
    while (i < size):
        if data[i].__contains__(".locals"):
            current_val = data[i].split(".locals")[1].strip("\n")
            new_val = int(current_val) + 3

            if new_val > 15:  # If it is more than v15: return
                return

            data[i] = ".locals " + str(new_val) + "\n"

            selected_var_1 = "v" + str(random.randint(int(current_val) + 1, new_val - 1))
            selected_var_2 = "v" + str(random.randint(int(current_val) + 1, new_val - 1))
            selected_var_3 = "v" + str(random.randint(int(current_val) + 1, new_val - 1))
            while selected_var_1 == selected_var_2 or selected_var_1 == selected_var_3 or selected_var_2 == selected_var_3:
                selected_var_1 = "v" + str(random.randint(int(current_val) + 1, new_val - 1))
                selected_var_2 = "v" + str(random.randint(int(current_val) + 1, new_val - 1))
                selected_var_3 = "v" + str(random.randint(int(current_val), new_val - 1))
            random_val_hex_1 = hex(random.randint(-8, 7))
            declaration_1 = "const/4 " + str(selected_var_1) + ", " + str(random_val_hex_1) + "\n"

            random_val_hex_2 = hex(random.randint(-8, 7))
            declaration_2 = "const/4 " + str(selected_var_2) + ", " + str(random_val_hex_2) + "\n"

            random_val_hex_3 = hex(random.randint(-8, 7))
            declaration_3 = "const/4 " + str(selected_var_3) + ", " + str(random_val_hex_3) + "\n"

            cond_var = ":cond_" + str(random.randint(100, 1000)) + "\n"
            if_statement = "if-ne " + selected_var_1 + "," + selected_var_2 + "," + cond_var + "\n"

            data.insert(i + 1, cond_var)

            # Insert Junk Code
            junkCode = []
            junkCode = generateMathJunk(current_val, new_val - 1)
            for code in junkCode:
                data.insert(i + 1, code)

            data.insert(i + 1, if_statement)
            data.insert(i + 1, declaration_1)
            data.insert(i + 1, declaration_2)
            data.insert(i + 1, declaration_3)

        size = len(data)
        i += 1


# Code Segementation is broken
def code_segmentation(data, switch_var):
    flag = None
    counter = 0
    return_flag = None
    pswitch_db = []
    packed_switch_db = []
    size = len(data)
    i = 0
    while (i < size):
        if data[i].__contains__(".method"):
            flag = 1
        elif data[i].__contains__("return") and flag == 1:
            return_flag = i
            flag = 0
        elif flag == 1:  # scrap all the necessary information
            if re.search("^:pswitch_[0-9]*", data[i]):
                pswitch_db.append(
                    str(re.findall("^:pswitch_[0-9]*", data[i])[0]))

        if flag == 0:

            # form the goto
            var = "v" + (switch_var[counter]) + ","
            packed_switch_db.append(":goto_switch\n")
            packed_switch_db.append("add-int/lit8 " + var + var + "0x1\n")
            for x in range(len(packed_switch_db)):
                data.insert(return_flag, packed_switch_db[x])
                return_flag += 1

            packed_switch_db.clear()

            # form the pswitch_data
            packed_switch_db.append(":pswitch_data_" + pswitch_string[counter] + "\n")
            packed_switch_db.append(".packed-switch 0x1\n")
            for line in pswitch_db:
                packed_switch_db.append(line + "\n")
            packed_switch_db.append(".end packed-switch\n")
            for x in range(len(packed_switch_db) - 1, -1, -1):
                data.insert(return_flag + 1, packed_switch_db[x])

            pswitch_db.clear()
            packed_switch_db.clear()

            counter += 1
            flag = None
        size = len(data)
        i += 1


# Misc Function
def generateStrJunk():
    string = []
    minLimit = random.randint(50, 100)
    maxLimit = random.randint(100, 200)
    for i in range(minLimit, maxLimit):
        rand_String_Length = random.randint(100, 1000)
        dataString = getRandstring(rand_String_Length)
        string.append('"' + dataString + '"')

    return string


def getRandstring(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def reshuffle(data, startIndex, endIndex):
    new_data = [None] * len(data)
    shuffle_hold = [None] * len(data)
    temp = 0
    # Add in the necessary first
    for i in range(len(startIndex)):
        start_hold = startIndex[i]
        end_hold = endIndex[i]
        new_data[start_hold] = data[start_hold]
        new_data[end_hold] = data[end_hold]

        for x in range(temp, start_hold):
            new_data[x] = data[x]
        temp = end_hold

    for i in range(len(startIndex)):
        start_hold = startIndex[i]
        end_hold = endIndex[i]
        shuffle = []
        counter = 0
        for x in range(start_hold + 1, end_hold):
            shuffle.append(data[x])

        random.shuffle(shuffle)

        for x in range(start_hold + 1, end_hold):
            if shuffle[counter] is not None:
                shuffle_hold[x] = shuffle[counter]
            counter += 1

        for x in range(start_hold + 1, end_hold):
            if new_data[x] is None:
                new_data[x] = shuffle_hold[x]

    # Replace the entire data
    for i in range(len(data) - 1):
        if new_data[i] is not None:
            data[i] = new_data[i]


def generateMathJunk(current, final):
    no_of_line = random.randint(900, 1000)
    instruction = []
    for i in range(no_of_line):
        var_0 = "v" + str(random.randint(int(current), final))
        var_1 = "v" + str(random.randint(int(current), final))
        var_2 = "v" + str(random.randint(int(current), final))
        add = "add-int " + var_0 + "," + var_1 + "," + var_2 + "\n"
        sub = "add-int " + var_0 + "," + var_1 + "," + var_2 + "\n"
        mul = "mul-int " + var_0 + "," + var_1 + "," + var_2 + "\n"
        instruction.append(add)
        instruction.append(sub)
        instruction.append(mul)

    return instruction

def unpacking(APK):
    name = os.path.basename(APK)
    name = name.split(".apk")[0]
    folder = "decodeAPK"
    os.system("java -jar apktool.jar -f d " + APK + " -o decodeAPK")
    return name, folder


def packing(name):
    os.system("java -jar apktool.jar -f b decodeAPK -o " + name + ".apk")


def locate(path):
    fileList = []
    for root, sub, files in os.walk(path):
        for file in files:
            if ("\com\\" in root) and ("\google\\" not in root)  and ("R$" not in file) and (file != "BuildConfig.smali") and (file != "R.smali"):
            # if ("\com\\" in root) and ("\google\\" not in root) and ("R$" not in file) and (file != "R.smali"):
                path = root+"\\"+file
                fileList.append(path)
    return fileList

def obfuscate(data):
    removeline(data)
    unreachable(data)
    insertjunk(data)
    reorder(data)

def write(data):
    for i in data:
        print (i)

def getFileName(APKpath):
    nameAPK = APKpath
    # Decompile the apk

    name,folder = unpacking(nameAPK)
    # Extract the filename from the apk
    name = name+"-obfuscated"

    # Locate all the main .smali
    fileList = locate(folder)
    return name, folder, fileList



def main_obfuscation(file):

    # Obfuscate every file inside the list
    data = open(file,"r").readlines()  #List
    obfuscate(data)

    obfuscatedOutput = ""
    for i in data:
        obfuscatedOutput += str(i) + "\n"

    return file, obfuscatedOutput