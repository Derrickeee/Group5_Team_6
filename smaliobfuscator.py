import re
import os

def inplace_edit_file(file_name: str):
    """
    Allow for a file to be replaced with new content.
    Yield a tuple of (readable, writable) file objects, where writable replaces
    readable. If an exception occurs, the old file is restored, removing the
    written data.
    """
    backup_file_name = "{0}{1}{2}".format(file_name, os.extsep, "bak")

    try:
        os.unlink(backup_file_name)
    except OSError:
        pass
    os.rename(file_name, backup_file_name)

    readable = open(backup_file_name, "r", encoding="utf-8")
    try:
        perm = os.fstat(readable.fileno()).st_mode
    except OSError:
        writable = open(file_name, "w", encoding="utf-8", newline="")
    else:
        os_mode = os.O_CREAT | os.O_WRONLY | os.O_TRUNC
        if hasattr(os, "O_BINARY"):
            os_mode |= os.O_BINARY
        fd = os.open(file_name, os_mode, perm)
        writable = open(fd, "w", encoding="utf-8", newline="")
        try:
            if hasattr(os, "chmod"):
                os.chmod(file_name, perm)
        except OSError:
            pass
    try:
        yield readable, writable
    except Exception as e:
        try:
            os.unlink(file_name)
        except OSError:
            pass
        os.rename(backup_file_name, file_name)

        print(
            'Error during inplace editing file "{0}": {1}'.format(file_name, e)
        )
        raise
    finally:
        readable.close()
        writable.close()
        try:
            os.unlink(backup_file_name)
        except OSError:
            pass

def get_junk_method(file_name: str):  # Return the junk method
    try:

        new_file_name = os.path.join(os.path.dirname(__file__), "resources", file_name)
        with open(new_file_name, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print('Error during reading file "{0}": {1}'.format(file_name, e))
        raise

def junk_method(self, smali_file: str):
    try:
        print(
            'Junk methods in file "{0}"'.format(smali_file)
        )
        """add to each smali class file the junk method"""
        with inplace_edit_file(smali_file) as (in_file, out_file):
            for line in in_file:
                out_file.write(line)
                if re.search(r'^([ ]*?)# direct methods',
                             line) is not None:  # At the top of the direct methods section
                    out_file.write(get_junk_method("junkMethod.txt"))  # add the junk method
    except Exception as e:
        print(
            'Error during execution of method renaming: {0}'.format(e)
        )
        raise

def addjunkcode(smaliCode):
    counter = 0
    saltNOP = "nop\n\n"

    # reset iterator [ Salt with NOP ]
    iterator = 0
    with open(smaliCode, "r") as fp:
        lines = fp.readlines()
        while iterator < len(lines):
            if ".method" in lines[iterator]:
                randint = random.randint(3, 5)
                for i in range(1, randint):
                    lines.insert(iterator + i, saltNOP)
                iterator += 1
            if "if-le" in lines[iterator]:
                check = [int(check) for check in re.findall(r'-?\d+\.?\d*', lines[iterator])]
                try:
                    if int(check[2]) > 500:
                        randint = random.randint(3, 5)
                        for i in range(1, randint):
                            lines.insert(iterator + i, saltNOP)
                except:
                    pass
                iterator += 1
            iterator += 1
    f = open(smaliCode, "w")
    f.writelines(lines)
    f.close()

    # reset iterator [ Salt with goto junk ]
    iterator = 0
    with open(smaliCode, "r") as fp:
        lines = fp.readlines()
        while iterator < len(lines):
            if "nop" in lines[iterator]:
                anotherRand = random.randint(1, 3)
                for i in range(0, anotherRand):
                    saltGOTOfront = "goto : gogo_" + str(counter) + "\n"
                    saltGOTOback = ": gogo_" + str(counter) + "\n\n"
                    lines.insert(iterator + i, saltGOTOfront)
                    lines.insert(iterator + 1 + i, saltGOTOback)
                    counter += 1
                    iterator += 2
            iterator += 1
    f = open(smaliCode, "w")
    f.writelines(lines)
    f.close()
        
