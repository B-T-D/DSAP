"""Test-discovery helper. Modifies sys.path according to the OS of the
environment in which the tests are being run."""

import os, sys
from pathlib import Path

this_filename = Path(__file__).name

assert (this_filename.startswith("test") or this_filename.endswith("test.py")),\
"Test discovery helper's filename must start or end with 'test'"
# Otherwise pytest won't run it. 

if os.name == "nt": # If windows use backslash
    for subdirectory in os.scandir():
        sys.path.append(os.path.abspath(subdirectory.name + "\\"))
else: # in TravisCI default env specifically, os.name evaluates to str "posix"
    for subdirectory in os.scandir():
        sys.path.append(os.path.abspath(subdirectory.name+ "/"))

print(f"Test-discovery helper '{this_filename}' ran")
