#!/usr/bin/env python3
import sys 
import re
import os

print("\033[94m-- Increment Cargo.toml Version: v0.1.0 --")                        # print version
print("\033[92m[INFO] \x1b[0mRunning git pull...")                                                       
os.system('git --git-dir=' + sys.path[0] + '/.git pull')                           # update the git repo
os.system('cd ' + os.getcwd())                                                     # change to original dir

try: 
    with open ("Cargo.toml", "r") as cargo_toml:
        regex = r"^([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"

        file = cargo_toml.read()                                                    # open file for reading
        ver_idx = file.find("version")                                               # find first occurrence of "version"
        ver_num_s = file.find("\"", ver_idx)                                         # find start of version number
        ver_num_e = file.find("\"", file.find("\"", ver_idx) + 1)                      # find end of version number
        
        ver_num = file[int(ver_num_s) + 1 : int(ver_num_e)]                         # slice out version number and remove first quote

        major = ver_num[0:ver_num.find(".")]                                        # find major number
        minor = ver_num[ver_num.find(".")+1:ver_num.find(".", ver_num.find(".")+1)]   # find minor number  
        patch = ver_num[ver_num.find(".", ver_num.find(".")+1)+1:]    
        old_ver = str(major) + "." + str(minor) + "." + str(patch)                 # record old version

        if sys.argv[1] == '-m' or sys.argv[1] == '-major':                         # if major increase
            major = int(major) + 1
            minor = 0
            patch = 0
            # print(new_major)
        elif sys.argv[1] == '-n' or sys.argv[1] == '-minor':                       # if minor increase
            minor = int(minor) + 1
            patch = 0
            # print(new_minor)
        elif sys.argv[1] == '-p' or sys.argv[1] == '-patch':                       # if patch increase
            patch = int(patch) + 1
            # print(new_patch)
        elif sys.argv[1] == '-v' or sys.argv[1] == "-version":                     # if version declared
            if re.match(regex, sys.argv[2]): 
                set_ver = sys.argv[2]
            else :
                print("\033[91m[ERROR] \x1b[0mVersion not SemVer. Cancelling...")
                sys.exit()
        else :
            print("\033[91m[ERROR] \x1b[0mIncorrect argument. Cancelling...")
            sys.exit()

        try: set_ver
        except NameError:
            new_ver = str(major) + "." + str(minor) + "." + str(patch)             # construct new version string
        else:
            new_ver = set_ver

        new_file = file.replace(old_ver, new_ver)                                    # replace old version string
        cargo_file = open("Cargo.toml", "w")                                        # open cargo file for editing
        cargo_file.write(new_file)                                                   # write new files contents
        cargo_file.close()                                                          # close writer

        print("\033[92m[INFO] \x1b[0mUpdated version string from: " + old_ver + " to: " + new_ver)       # log increment
except FileNotFoundError:
    print("\033[91m[ERROR] \x1b[0mNo Cargo.toml found!")
except IndexError:
    print("\033[91m[ERROR] \x1b[0mNo argument passed!")