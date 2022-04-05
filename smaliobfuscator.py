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
