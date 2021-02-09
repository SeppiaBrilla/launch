#!/usr/bin/python3
import sys
import os


def find_file(file_name):
    for file in os.listdir('./'):
        if(file == file_name):
            return True
    return False

def find_option_in_file(option_name):
    if not find_file(".launch"):
        return False
    f = open(".launch", "r")
    for line in f:
        if option_name == line.split()[0]:
            return True
    return False

def prompt(text):
    return input(text + " Y/N ").capitalize() == "Y" 

def option(args):
    if "-" == args[1][0]:
        settings(args)
    else:
        read(args[1])

def settings(args):
    if not find_file(".launch") and args[1]!= "-help" and args[1]!= "-new":
        print(".launch file not found, please create one whit the -new option or use the -help option if you want help")
        return
    if not args[1] in allSettings:
        print("option not found, please use the -help option if you want help")
        return
    if allSettings[args[1]](args):
        print("not enough arguments, please use the -help option if you want help")

def new(args):
    if len(args) < 5:
        return 1
    if find_file(".launch"):
        if find_option_in_file(args[2]):
            print("there's already an option with this name, abort")
            return
        f = open(".launch","a")
        f.write(args[2]+" "+args[3]+" "+args[4] + "\n")
        f.close()
    else:
        if not prompt("I've not found a .launch file, do you want me to create one?"):
            print("abort")
            return 0
        if find_file(".gitignore"):
            if prompt("do you want me to update your gitignore?"):
                git = open(".gitignore","a")
                git.write(".launch")
                git.close()
        f = open(".launch","w")
        f.write(args[2]+" "+args[3]+" "+args[4] + " --default\n")
        f.close()
    return 0

def remove(args):
    if len(args) < 3:
        return 1
    with open(".launch", "r") as f:
        lines = f.readlines()
        with open(".launch", "w") as f:
            for line in lines:
                if "--default" == line.split()[len(line.split()) - 1] and line.split()[0] == args[2]:
                    if not prompt("You are deleting the defaut option, are you sure?"):
                        f.write(line)
                elif line.split()[0] != args[2]:
                    f.write(line)

def rename(args):
    if len(args) < 4:
        return 1
    if find_option_in_file(args[3]):
        print("there's already an option with this name, abort")
        return
    with open(".launch", "r") as f:
        lines = f.readlines()
        with open(".launch", "w") as f:
            for line in lines:
                if line.split()[0] != args[2]:
                    f.write(line)
                else:
                    new_line = line.split()
                    new_line[0] = args[3]
                    new_line = ' '.join(new_line)
                    if prompt("    do you want to change line :\n" + line + "\n   to:\n" + new_line + "\n   ?"):
                        f.write(new_line + "\n")
                    else:
                        f.write(line)
                    

def mkdflt(args):
    if len(args) < 3:
        return 1
    with open(".launch", "r") as f:
        lines = f.readlines()
        with open(".launch", "w") as f:
            for line in lines:
                if line.split()[0] != args[2] and line.split()[len(line.split()) - 1] != "--default":
                    f.write(line)
                elif line.split()[0] != args[2] and line.split()[len(line.split()) - 1] == "--default":
                    if prompt("the option: " +line.split()[0] + " will not be the default one anymore, are you sure?"):
                        line = line.split()
                        line[len(line) - 1] = ""
                        f.write(" ".join(line) + "\n")
                    else:
                        print("abort")
                elif line.split()[0] == args[2] and line.split()[len(line.split()) - 1] == "--default":
                        print("already the defaut option")
                else:
                    line = line[:-1] + " --default\n"
                    f.write(line)
    return 0

def help(args):
    print("Hi, thanks for have installed launch, this program will help you to create macro that call a program with a set of arguments for you! Here's how:")
    print("-------------------------------------------------------------------------------------------------------------------------------------------------") 
    print("you can just call lauch without arguments, it will just call the default option")
    print("you can call launch <option name> to call a specific option")
    print("-------------------------------------------------------------------------------------------------------------------------------------------------")
    print("use -new add an option to your .lauch file (you can also -new to create a new -lauch file if not present in folder)")
    print("    usage: -new <new option name> <program to call> <file argument of the program>")
    print("you can also call the program with a sets of arguments or none. To have a sets of arguments just list them all separated by a '%20$', if you want to have no arguments just write '%20%'")
    print("-------------------------------------------------------------------------------------------------------------------------------------------------")
    print("use -remove to remove an already existing option")
    print("    usage: -remove <option name>")
    print("-------------------------------------------------------------------------------------------------------------------------------------------------")
    print("use -rename to rename an already exixsting option")
    print("    usage: -rename <old name> <new name>")
    print("-------------------------------------------------------------------------------------------------------------------------------------------------")
    print("use mkdflt to change the defaut option, if there's one, or create it if not")
    print("    usage: -mkdflt <option name>")
    print("-------------------------------------------------------------------------------------------------------------------------------------------------")

def read(called):
    if not find_file(".launch"):
        print(".launch file not found, please create whit the -new option one or use the -help option if you want help")
        return
    f = open(".launch", "r")
    for line in f:
        splitted = line.split()
        if called == splitted[0] or (called == splitted[len(splitted) - 1] and called == "--default"):
            os.system(splitted[1] + " " + " ".join(splitted[2].split("%20%")))
            f.close()
            return
    f.close()

def main():
    if len(sys.argv) > 1:
        option(sys.argv)
    else:
        read("--default")

allSettings = {"-new": new, "-remove":remove, "-rename": rename, "-mkdflt": mkdflt, "-help": help}

if __name__=="__main__":
    main()

