import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("init", help="initialize spwn library project")
parser.add_argument("name", help="name of spwn library project")

args = vars(parser.parse_args())

def main():
    if os.listdir('.'):
        raise BaseException("Error: CWD must be empty")

    LIBNAME = args['name']
    
    os.makedirs(f"libraries/{LIBNAME}/src")

    with (
        open("main.spwn", 'w+') as mainf,
        open(f"libraries/{LIBNAME}/lib.spwn", "w+") as libf,
        open(".gitignore", "w+") as gitigf
    ):
        mainf.write(f"import {LIBNAME}")
        libf.write("")
        gitigf.write("main.spwn")
    
    os.system("git init") # yes i know os.system is deprecated

if __name__ == "__main__":
    main()
