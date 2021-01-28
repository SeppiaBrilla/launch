#!/usr/bin/python3
import sys
import os

def find_file():
    for file in os.listdir('./'):
        if(file == ".launch"):
            return True
    return False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-new" and len(sys.argv) == 5:
        if(find_file()):
            f = open(".launch","a")
            f.write(sys.argv[2]+" "+sys.argv[3]+" "+sys.argv[4])
            f.close()
        else:
            f = open(".launch","w")
            f.write(sys.argv[2]+" "+sys.argv[3]+" "+sys.argv[4])
            f.close()
    elif len(sys.argv) != 5:
        print("errore, troppi pochi argomenti")


    
if __name__=="__main__":
    main()

