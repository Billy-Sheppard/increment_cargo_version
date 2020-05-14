#!/usr/bin/env python3
import sys 
import re
import os

print("\033[94m-- Increment Cargo.toml Version: v0.1.1 --")                        # print version
print("\033[92m[INFO] \x1b[0mRunning git pull...")                                                       
os.system('git --git-dir=' + sys.path[0] + '/.git pull')                           # update the git repo
os.system('cd ' + os.getcwd())                                                     # change to original dir

try: 
    if '-r' in sys.argv:                                                           # if -r present
        folder = "rust/"                                                           # look in folder rust/
    else:
        folder = ""                                                                # else look where run
    with open ((folder + "Cargo.toml"), "r") as cargo_toml:
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

        if '-m' in sys.argv or '-major' in sys.argv:                               # if major increase
            major = int(major) + 1
            minor = 0
            patch = 0
            # print(new_major)
        elif '-n' in sys.argv or '-minor' in sys.argv:                             # if minor increase
            minor = int(minor) + 1
            patch = 0
            # print(new_minor)
        elif '-p' in sys.argv or '-patch' in sys.argv:                             # if patch increase
            patch = int(patch) + 1
            # print(new_patch)
        elif '-v' in sys.argv or "-version" in sys.argv:                           # if version declared
            try:
                idx = sys.argv.index('-v')
            except: 
                idx = sys.argv.index('-version')

            if re.match(regex, sys.argv[idx+1]): 
                set_ver = sys.argv[idx+1]
            else :
                print("\033[91m[ERROR] \x1b[0mVersion not SemVer. Cancelling...")
                sys.exit()
        elif '-h' in sys.argv or "-help" in sys.argv: 
            print("\n\n\033[94m-- Increment Cargo.toml Version Help --\x1b[0m")    
            print("\n\t-m: For major version increase")

            print("\n\t-n: For minor version increase")

            print("\n\t-p: For patch version increase")

            print("\n\t-v [version]: For specific version increase")
            print("\t\t• will only complete if a valid SemVer string (no quotes) is passed\n\n")
        else :
            print("\033[91m[ERROR] \x1b[0mIncorrect argument. Cancelling...")
            sys.exit()

        try: set_ver
        except NameError:
            new_ver = str(major) + "." + str(minor) + "." + str(patch)                                   # construct new version string
        else:
            new_ver = set_ver

        new_file = file.replace(old_ver, new_ver, 1)                                                       # replace old version string
        cargo_file = open("Cargo.toml", "w")                                                              # open cargo file for editing
        cargo_file.write(new_file)                                                                         # write new files contents
        cargo_file.close()                                                                                # close writer

        print("\033[92m[INFO] \x1b[0mUpdated version string from: " + old_ver + " to: " + new_ver)       # log increment

        if ("-t" in sys.argv or "-tag" in sys.argv) :                                                    # if -t flag is second
            os.system('cargo check')                                                                     # run cargo check to bump Cargo.lock
            os.system('git add Cargo.toml Cargo.lock')                                                   # add both files to a new commit
            os.system('git commit -m "v' + new_ver + '"')                                                # commit files with message v{version}
            os.system('git tag "v' + new_ver + '"')                                                      # tag commit with v{version}
            os.system('git push && git push --tags')                                                     # push commit and tags
            print("\033[92m[INFO] \x1b[0mAdded Cargo.toml and Cargo.lock to a commit and tagged commit: v" + new_ver)

except FileNotFoundError:
    try: 
        with open ("Version.toml", "r") as version_toml:
            regex = r"^([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"

            file = version_toml.read()                                                  # open file for reading
            ver_idx = file.find("version")                                               # find first occurrence of "version"
            ver_num_s = file.find("\"", ver_idx)                                         # find start of version number
            ver_num_e = file.find("\"", file.find("\"", ver_idx) + 1)                      # find end of version number
            
            ver_num = file[int(ver_num_s) + 1 : int(ver_num_e)]                         # slice out version number and remove first quote

            major = ver_num[0:ver_num.find(".")]                                        # find major number
            minor = ver_num[ver_num.find(".")+1:ver_num.find(".", ver_num.find(".")+1)]   # find minor number  
            patch = ver_num[ver_num.find(".", ver_num.find(".")+1)+1:]    
            old_ver = str(major) + "." + str(minor) + "." + str(patch)                 # record old version

            if '-m' in sys.argv or '-major' in sys.argv:                               # if major increase
                major = int(major) + 1
                minor = 0
                patch = 0
                # print(new_major)
            elif '-n' in sys.argv or '-minor' in sys.argv:                             # if minor increase
                minor = int(minor) + 1
                patch = 0
                # print(new_minor)
            elif '-p' in sys.argv or '-patch' in sys.argv:                             # if patch increase
                patch = int(patch) + 1
                # print(new_patch)
            elif '-v' in sys.argv or "-version" in sys.argv:                           # if version declared
                try:
                    idx = sys.argv.index('-v')
                except: 
                    idx = sys.argv.index('-version')

                if re.match(regex, sys.argv[idx+1]): 
                    set_ver = sys.argv[idx+1]
                else :
                    print("\033[91m[ERROR] \x1b[0mVersion not SemVer. Cancelling...")
                    sys.exit()
            elif sys.argv == '-h' or sys.argv == "-help": 
                print("\n\n\033[94m-- Increment Cargo.toml Version Help --\x1b[0m")    
                print("\n\t-m: For major version increase")

                print("\n\t-n: For minor version increase")

                print("\n\t-p: For patch version increase")

                print("\n\t-v [version]: For specific version increase")
                print("\t\t• will only complete if a valid SemVer string (no quotes) is passed\n\n")
            else :
                print("\033[91m[ERROR] \x1b[0mIncorrect argument. Cancelling...")
                sys.exit()

            try: set_ver
            except NameError:
                new_ver = str(major) + "." + str(minor) + "." + str(patch)                                   # construct new version string
            else:
                new_ver = set_ver

            new_file = file.replace(old_ver, new_ver, 1)                                                       # replace old version string
            version_file = open("Version.toml", "w")                                                          # open cargo file for editing
            version_file.write(new_file)                                                                       # write new files contents
            version_file.close()                                                                              # close writer

            print("\033[92m[INFO] \x1b[0mUpdated version string from: " + old_ver + " to: " + new_ver)       # log increment
            if len(sys.argv) > 2 :
                if ("-t" in sys.argv or "-tag" in sys.argv) :                                                # if -t flag exists
                    os.system('git add Version.toml')                                                        # add Version.toml to a new commit
                    os.system('git commit -m "v' + new_ver + '"')                                            # commit files with message v{version}
                    os.system('git tag "v' + new_ver + '"')                                                  # tag commit with v{version}
                    os.system('git push && git push --tags')                                                 # push commit and tags
                    print("\033[92m[INFO] \x1b[0mAdded Cargo.toml and Cargo.lock to a commit and tagged commit: v" + new_ver)

    except FileNotFoundError:
        print("\033[91m[ERROR] \x1b[0mNo Cargo.toml or Version.toml found!")

except IndexError:
    print("\033[91m[ERROR] \x1b[0mNo argument passed!")