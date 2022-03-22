import re
import secrets
import os


def getMethodName(line):
    res = None
    if re.search(
            '(public\s|private\s)?(static\s|final\s)?(void|int|String|boolean|byte|char|short|long|float|double|File)\s\w+\(.*\)',
            line):
        res = re.search('\s(\w+)\(.*\)', line).group(1)
    return res


def getVarName(line):
    res = None
    if re.search('(public\s|private\s)?(static\s|final\s)?[a-zA-Z<>\[\]]*\s[a-zA-Z]\w*\s?[,=;\)]\s?', line):
        res = re.findall('[a-zA-Z<>\[\]]*\s([a-zA-Z]\w*)\s?[,=;\)]', line)
    return res


def getSoutLn(line):
    res = None
    res = re.findall('System.out.println\(\".+?\"\)\;', line)
    return res


def getImport(lineArr):
    res = []
    exist = None
    for line in lineArr:

        if (re.search('import.+?;', line)):
            res.append(line)
    return res


def removeComment(line, count):
    if count == 1:
        # Check if */
        if re.search('(.*)?(\*\/)(.*)?', line):
            count = 0
        # Remove line
        line = ""
    else:
        # Check if //
        if re.search('.*(\/\/)', line):
            line = ""

        # Check if /*
        if re.search('(.*)?(\/\*)(.*)?', line):
            count = 1
            # Check if */ within same line
            if re.search('(.*)?(\*\/)(.*)?', line):
                count = 0
            # Remove line
            line = ""
    return line, count


def removeLog(line):
    if re.search('android\.util\.Log\.[a-z]+.*', line):
        line = ""
    if re.search('Log\.[a-z]+.*', line):
        line = ""
    return line


def renameVar(inputFilePath, outputFilePath):
    methodNameDict = {}
    varNameDict = {}
    counter = 1
    count = 0  # Check if multiline comment. 1 if within comments

    # Create output file
    outFile = open(outputFilePath, "w", encoding="utf-8")

    # Open file
    with open(inputFilePath) as javaFile:
        for line in javaFile:
            # METHOD
            methodName = getMethodName(line)
            if methodName is not None and methodName != ("main" or "Main"):
                # Create string to replace method name
                word = '$' + ('\u200E' * counter)
                methodNameDict[methodName] = word
                # increment counter for number of \u200E to add
                counter += 1

            # VARIABLE
            varName = getVarName(line)
            if varName is not None:
                for i in varName:
                    # Make sure variable is not break or continue
                    if i != ("break" or "continue"):
                        # Create string to replace variable name
                        word = '$' + ('\u200E' * counter)
                        varNameDict[i] = word
                        # increment counter for number of \u200E to add
                        counter += 1

        # Set file pointer back to start
        javaFile.seek(0)

        for line in javaFile:
            # Get line and
            line, newcount = removeComment(line, count)
            count = newcount

            # Remove all logs
            line = removeLog(line)

            # Get method name and random word value in dictionary
            for method, new in methodNameDict.items():
                # (public) (static) <type> name (){
                initialMethod = re.match(
                    rf'(\s+)?(public\s|private\s)?(static\s|final\s)?(void|int|String|boolean|byte|char|short|long|float|double|File)\s({method})',
                    line)
                # method() or a.method()
                callMethod = re.match(rf'(\s+)?(\w+)?[^super\.](.*\=.*)?\.?({method})\(.*\)', line)

                if initialMethod or callMethod is not None:
                    line = re.sub(rf'({method})', new, line)

            # Get variable name and random word value in dictionary
            for variable, new in varNameDict.items():
                varFound = re.search(rf'{variable}', line)

                if varFound is not None:
                    line = re.sub(rf'\b{variable}\b', new, line)
            outFile.write(line)

    # Close files that are not used
    outFile.close()
    javaFile.close()


def obfSoutLn(soutLn):
    tempStr = ""
    charArr = list(soutLn)

    for char in charArr:
        tempStr += r'\\u{:04X}'.format(ord(char))

    return tempStr


def obfSoutStr(soutStr):
    tempArr = []
    tempStr = ""
    flag = False

    splitArr = soutStr.split("+")

    for string in splitArr:

        if (re.search('\"([^\"]*)\"', string)):

            for char in string:

                if not (char == "\"" or char == ")" or char == ";" or char == " "):

                    if (flag == True and (char == "n")):
                        print("found \\n")

                        flag = False
                        tempStr += "\\\\n"

                    elif (flag == False and char == "\\"):

                        flag = True

                    elif (flag == True):

                        flag = False
                        tempStr += "\\u005C" + (oct(ord(char))).replace("0o", "\\\\")

                    else:

                        flag = False
                        randNum = secrets.randbelow(3)

                        if (randNum == 0):

                            tempStr += (oct(ord(char))).replace("0o", "\\\\")

                        elif (randNum == 1):

                            tempStr += r'\\u{:04X}'.format(ord(char))

                        else:
                            asciiDec = ord(char)

                            tempStr += "\"\\\\u002B(c\\\\u0068ar\\\\u0029" + "\\\\u0028\\\\u002D~\\\\u002D\\\\u007E" + str(
                                asciiDec - 1) + "-1)\\\\u002B\""

                else:

                    tempStr += r'\\u{:04X}'.format(ord(char))

            tempArr.append(tempStr)

            tempStr = ""

        else:

            for char in string:
                tempStr += r'\\u{:04X}'.format(ord(char))

            tempArr.append(tempStr)

            tempStr = ""

    return "\\\\u002B".join(tempArr)


def addUnicode(line):
    splitArr = line.split("(")

    obfSout = obfSoutLn(splitArr[0])

    obfStr = obfSoutStr(splitArr[1])

    return "\\\\u0028".join([obfSout, obfStr])


def runObfSout(inFile, outFile):
    # TODO CHANGE TO RELEVANT INPUT AND OUTPUT
    filename = inFile
    tempOutFile = open("./uploads/temp.txt", "w", encoding="utf-8")
    soutNameDict = {}

    with open(filename, 'r', encoding="utf-8") as javaFile:

        for line in javaFile:
            soutLn = getSoutLn(line)
            if soutLn is not None:
                for i in soutLn:
                    soutNameDict[i] = addUnicode(i)

            for sout, new in soutNameDict.items():
                line = re.sub(rf'({re.escape(sout)})', new, line)

            tempOutFile.write(line)

    tempOutFile.close()
    # TODO CHANGE TO OUTPUT FILE
    if (os.path.isfile(outFile)):
        os.remove(outFile)

    # TODO CHANGE TO OUTPUT FILE DUN Change temp.txt
    os.rename(r'./uploads/temp.txt', outFile)


def runObfImport(inFile, outFile):
    # TODO CHANGE TO RELEVANT INPUT AND OUTPUT
    filename = inFile
    tempOutFile = open("./uploads/temp.txt", "w", encoding="utf-8")

    with open(filename, "r", encoding="utf-8") as File:
        impNameDict = {}

        lines = File.readlines()  # lines is list of line, each element '...\n'
        test = "/*\n"
        test2 = "\nTo Delete\n\\u002A\\u002F"

        lines.insert(0, test)  # you can use any index if you know the line index
        lines.insert(1, test2)
        temp = 0

        importName = getImport(lines)
        if importName is not None:
            for i in importName:
                obfCode = obfImport(i)
                impNameDict[i] = obfCode

        for imp, new in impNameDict.items():
            for i, line in enumerate(lines):
                # print(line)
                if (re.search(rf'({re.escape(imp)})', line)):
                    print(i)
                    temp = i
                lines[i] = re.sub(rf'({re.escape(imp)})', new, line)

        test3 = "\n"
        test4 = "\\u002F\\u002A\n"
        test5 = "\n*/ \n"
        # lines.insert(temp, "asd")
        lines.insert(temp, test3)
        lines.insert(temp + 2, test4)
        lines.insert(temp + 3, test5)
        # javaFile.seek(0)                 # file pointer locates at the beginning to write the whole file again
        tempOutFile.writelines(lines)  # write whole lists again to the same file

    tempOutFile.close()
    File.close()

    # TODO CHANGE TO OUTPUT FILE
    if (os.path.isfile(outFile)):
        os.remove(outFile)

    # TODO CHANGE TO OUTPUT FILE DUN Change temp.txt
    os.rename(r'./uploads/temp.txt', outFile)


def obfImport(line):
    tempStr = ""
    charArr = list(line)

    for char in charArr:
        tempStr += r'\\u{:04X}'.format(ord(char))

    return tempStr


def main(inFile, outFile):
    renameVar(inFile, outFile)
    runObfImport(outFile, outFile)
    runObfSout(outFile, outFile)


if __name__ == "__main__":
    main('./java/Example/test1.java', './uploads/testing2.java')