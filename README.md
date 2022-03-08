# SIT ICT 2207 AY20/21 Mobile Security Project 
This is a Year 2 Trimester 2 ICT 2207 - Mobile Security Project. This project's objective is to design and develop smart obfuscation algorithms to prevent the reverse engineering of Android APKs. 

The tool is able to take in and obfuscate both Java and Smali code that the user inputs via a web Graphical User Interface (GUI). Android applications can be reverse engineered for undesirable purposes, such as allowing others to inject malicious code into the application for malicious purposes, or copying and duplicating the application for their own resale. In order to counter this, it is important to obfuscate the codes that one writes to conceal its purpose. This protects the application from potential tampering and misuse. 

## Getting Started
- Download the project into a folder of your choice
- Install and run this project in Python3 Environment

## Dependencies Installation
To install the tools, enter `pip install -r requirements.txt` in python console/terminal to install the necessary dependencies for the project

## Usage
To run the tool, enter either of the following commands in python console/terminal under the project root directory
1. `set FLASK_APP=app.py` followed by `flask run`; or
2. `python3 app.py`

### Features 
- APK file handling: When a file uploaded is an APK file, the options available are: decompile, and obfuscate and recompile. The decompiling and recompiling functions utilizes Apktool for its operation. (For obfuscation and recompilation, find the MainActivity.smali in smali folder) 
- Java source code obfuscation: The program is able to accept Java source code files for it to obfuscate. The techniques used are: encoding, renaming variables and methods, and removing debugging information.
- Smali code obfuscation: The program is used for obfuscating the smali file are by doing try-catch obfuscation, adding of “nop” instructions, and removing debugging information. 

### Compiling Java with Android Studio
1. Locate the module `build.gradle` in the application folder
2. Edit the `compileOptions` to include `encoding "IBM00858"`

![Gradle compileOptions](https://i.ibb.co/x8SwpRM/Picture1.png)


## References 
- https://github.com/ClaudiuGeorgiu/Obfuscapk/blob/master/src/obfuscapk/resources/nop_valid_op_codes.txt
- http://pallergabor.uw.hu/androidblog/dalvik_opcodes.html
- https://www.sciencedirect.com/science/article/pii/S0167404816300529
- https://dr.ntu.edu.sg/bitstream/10356/105732/1/SCE13073_NGUYEN%20DINH%20PHUC.pdf
- https://flask.palletsprojects.com/en/1.1.x/
- https://realpython.com/flask-by-example-part-1-project-setup/

## Authors

