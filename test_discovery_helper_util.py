"""Test-discovery helper. Modifies sys.path according to the OS of the
environment in which the tests are being run."""

import os, sys

if os.name == "nt": # If windows use backslash
    for subdirectory in os.scandir():
        sys.path.append(os.path.abspath(subdirectory.name + "\\"))
else: # in TravisCI default env specifically, os.name evaluates to str "posix"
    for subdirectory in os.scandir():
        sys.path.append(os.path.abspath(subdirectory.name+ "/"))

print(f"Test-discovery helper '{this_filename}' ran")
