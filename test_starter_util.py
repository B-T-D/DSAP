# Goal is for unittest to run this because it starts with "test".

import os, sys

print("teststarter util ran")

print(os.name)
this_directory = os.path.dirname(__file__)

if os.name == "nt":
    for subdirectory in os.scandir():
    ##    print(subdirectory.name)
        sys.path.append(os.path.abspath(subdirectory.name + "\\"))
elif os.name == "posix": # TravisCI env default os name
    for subdirectory in os.scandir():
        sys.path.append(os.path.abspath(subdirectory.name+ "/"))

