#!/usr/bin/python3
import sys 

with open ("Cargo.toml", "r") as myfile:
    file = myfile.read()                                                         # open file for reading
    ver_idx = file.find("version")                                               # find first occurance of "version"
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
    elif sys.argv[1] == '-n':                                                  # if minor increase
        minor = int(minor) + 1
        # print(new_minor)
    elif sys.argv[1] == '-p':                                                  # if patch increase
        patch = int(patch) + 1
        # print(new_patch)
    else :
        print("Incorrect argument. Cancelling...")
        sys.exit()

    new_ver = str(major) + "." + str(minor) + "." + str(patch)                 # construct new version string
    
    new_file = file.replace(old_ver, new_ver)                                    # replace old version string
    cargo_file = open("Cargo.toml", "w")                                        # open cargo file for editing
    cargo_file.write(new_file)                                                   # write new files contents
    cargo_file.close()                                                          # close writer

    print("Updated from: " + old_ver + " to: " + new_ver)                      # log increment
