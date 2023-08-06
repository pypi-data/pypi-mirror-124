import os
import random

def add_one(number):
    return number + 1

text = "obama"

def fp():
    nm = input("file path:")
    os.system("start "+nm)
    

def txt():
    print(input("text:"))

def pinst():
    module = input("(pip)name of module:")
    os.system("py -m pip install" + module)

def comm():
    com = input("py_T{command}:")

    if com == "ver":
        print(" ")
        print("1.1b - Version of Py_T (25.10.21)")
        print(" ")
        comm()

    if com == "text":
        print(" ")
        txt()
        print(" ")

    if com == "py_t.exitshell":
        quit()

    if com == "openfile":
        fp()

    if com == "sys.s_h":
        srsly = input("do you want to put the computer into sleep mode? Answer N / Y:")
        if srsly == "Y":
            os.system("shutdown /h")
        if srsly == "N":
            comm()

    if com == "zakon.likee_govno":
        print("malodec nashel pashalku , da kstati... ya s toboi soglasen!")

    if com == "py.pip_install":
        print(" ")
        pinst()
        print(" ")

    if com == "py_t.demogr":
        print("000000000000")
        print("0     000000")
        print("0     000000")
        print("0     000000")
        print("0 000000   0")
        print("0 0000000 00")
        print("0 0000000 00")
        print("000000000000")

    if com == "?":
        print("==")
        print(" ")
        print("|cmds|")
        print("comm() (opens cmd line)")
        print("py_t.exitshell")
        print("py_t.stopshell")
        print("py_t.demogr")
        print("openfile")
        print("text")
        print("ver")
        print("?")
        print("|cmds|")
        print(" ")
        print("type ?2 for help to importing py_term")
        print("==")

    if com == "?2":
        print("==")
        print(" ")
        print("for importing py_term to your program , copy the code:")
        print("|CODE|")
        print("import py_term")
        print("py_term.comm()")
        print("|CODE|")
        print(" ")
        print("type ? for view cmds list")
        print(" ")
        print("==")

        
    if not com == "py_t.stopshell":
        comm()

print("Py-Terminal by LayfikRus (1.1)")
print("type ? for view commands list")
      
