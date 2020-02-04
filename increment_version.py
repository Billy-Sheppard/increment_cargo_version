#!/usr/bin/python3
import sys 
import re

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

    if sys.argv[1] == '-m':                                                    # if major increase
        major = int(major) + 1
        # print(new_major)
        new_ver = str(major) + "." + str(minor) + "." + str(patch)             # construct new version string
    elif sys.argv[1] == '-n':                                                  # if minor increase
        minor = int(minor) + 1
        # print(new_minor)
        new_ver = str(major) + "." + str(minor) + "." + str(patch)             # construct new version string
    elif sys.argv[1] == '-p':                                                  # if patch increase
        patch = int(patch) + 1
        # print(new_patch)
        new_ver = str(major) + "." + str(minor) + "." + str(patch)             # construct new version string
    elif sys.argv[1] == '-v':                                                  # if version declared
        if re.match(regex, sys.argv[2]): 
            new_ver = sys.argv[2]
        else :
            print("Version not SemVer. Cancelling...")
            sys.exit()
    else :
        print("Incorrect argument. Cancelling...")
        sys.exit()

    
    new_file = file.replace(old_ver, new_ver)                                    # replace old version string
    cargo_file = open("Cargo.toml", "w")                                        # open cargo file for editing
    cargo_file.write(new_file)                                                   # write new files contents
    cargo_file.close()                                                          # close writer

    print("Updated from: " + old_ver + " to: " + new_ver)                      # log increment
