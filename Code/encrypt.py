import hashlib
import sys
import time
import threading
import uuid
import secrets
import psutil
from pathlib import Path
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def loading():
    global running
    width = 25
    block_size = 5 
    position = 0
    direction = 1 
    running = True

    while running:
        track = ['='] * width
        for i in range(block_size):
            if 0 <= position + i < width:
                track[position + i] = '#'
        sys.stdout.write(f"\r[{''.join(track)}]")
        sys.stdout.flush()
        
        position += direction
        if position == (width - 3) or position == -2:
            direction *= -1
        time.sleep(0.05) 

def read():
    global running
    name = input("Enter the username you want to retrieve:  ")
    path = (Path(__file__).resolve().parent).parent / "Data" / "Storage.txt"
    line = None

    with open(path, "r") as file:
        lines = file.readlines()

        for index, checking_name in enumerate(lines):
            if checking_name.strip().split("|")[0] == name:
                line = index
                break

    if line is not None:
        username, salt, strength, hashed_password = lines[line].strip().split("|")
        strength = int(strength)
        print("Username found")
        password_guess = input("password:  ")

        animation_thread = threading.Thread(target=loading)
        animation_thread.start()
        try:
            hashed_guess = Scrypt(salt=salt.encode('utf-8'), length=64, n=strength, r=8, p=1).derive(password_guess.encode('utf-8')).hex()
        finally:
            running = False
            animation_thread.join()
            print("")
        if secrets.compare_digest(hashed_guess, hashed_password):
            print("Password is correct")
            print(username, "Logged in successfully")    
    else:
        print("Username not found.")


def write():
    global running
    check = False
    username = input("username:  ")

    x = False
    while x == False:
        password = input("password:  ")
        reenter_password = input("reenter password:  ")
        if password == reenter_password:
            x = True
        else:
            print("Passwords do not match. Please try again.")

    x = False
    while x == False:
        print("Password strength: custom or auto")
        strength = input("strength:  ")
        if strength in ["custom", "auto"]:
            x = True

    if strength == "custom":
        
        ## Get strength unit
        x = False
        while x == False:
            print("unit: MB, GB")
            custom_strength_unit = input("unit:  ")
            if custom_strength_unit in ["MB", "GB"]:
                x = True

        ## Get strength amount
        x = False
        while x == False:
            print("strength must be a power of 2: (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024)")
            try:
                custom_strength_size = int(input(f"custom strength in {custom_strength_unit}:  "))
            except ValueError:
                continue
            if custom_strength_size in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:

                ## Gather RAM info to check safety
                memory = psutil.virtual_memory()
                ram = int(memory.available / 1024)
                ram_safe = ram * 0.25

                ## Make strength data usable
                if custom_strength_unit == "MB":
                    strength = custom_strength_size * 1024
                elif custom_strength_unit == "GB":
                    strength = custom_strength_size * 1024 * 1024
                
                if strength > ram_safe:

                    if strength > ram:
                        print("Strength exceeds available RAM.")

                    print("It is recommended to use a strength that is less than 25% of your available RAM.")
                    print("Available RAM: ", ram, "KB, ", ram / 1024, "MB, ", ram / 1024 / 1024, "GB")#

                    ## Recommend strength options
                    strength_defaults = [1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824]
                    strength_kb = int([kb for kb in strength_defaults if kb <= ram_safe][-1])
                    strength_mb = int(strength_kb / 1024)
                    strength_gb = int(strength_kb / 1024 / 1024)

                    print("Recommended strength: ", strength_kb, "KB, ", strength_mb, "MB, ", strength_gb, "GB")
                    print("Do you want to continue with the selected custom strength anyway? (y/n)")
                    continue_choice = input()
                    if continue_choice == "y":
                        x = True
                    else: 
                        x = False 
                        continue

                else:
                    x = True


    else:
        memory = psutil.virtual_memory()
        ram = memory.available / 1024

        if ram < 1024:
            check = True
            print("Warning: Your available RAM is less than 1MB. This may cause issues with hashing.")
            quit_choice = input("Do you want to exit the program? (y/n):  ")
            if quit_choice == "y":
                exit()
            else:
                print("Continuing with the program. Please be aware that the program may not function as intended.")


        ram = ram * 0.25
        strength_defaults = [1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824]
        try:
            strength = [kb for kb in strength_defaults if kb <= ram][-1]
        except IndexError:
            print("Error: No suitable strength found.")
            exit()

    if strength < 1024:
        strength = 1024
    if strength > 1073741824:
        strength = 1073741824

    if check == False:
        if ram*4 < 1024:
            print("Warning: Your available RAM is less than 1MB. This may cause issues with hashing.")
            quit_choice = input("Do you want to exit the program? (y/n):  ")
            if quit_choice == "y":
                exit()
            else:
                print("Continuing with the program. Please be aware that the program may not function as intended.")

    salt = str(uuid.uuid4())
    MAX_MEMORY = int(strength * 1024 * 1.5)

    animation_thread = threading.Thread(target=loading)
    animation_thread.start()
    try:
        hashed_password = Scrypt(salt=salt.encode('utf-8'), length=64, n=strength, r=8, p=1).derive(password.encode('utf-8')).hex()
    finally:
        running = False
        animation_thread.join()
        print("")

    print("Salt:", salt)
    print("Strength:", strength)
    print("Hashed password:", hashed_password)

    x = False
    while not x:
        password_guess = input("password:  ")
        animation_thread = threading.Thread(target=loading)
        animation_thread.start()
        try:
            hashed_guess = Scrypt(salt=salt.encode('utf-8'), length=64, n=strength, r=8, p=1).derive(password_guess.encode('utf-8')).hex()
        finally:
            running = False
            animation_thread.join()
            print("")
        if secrets.compare_digest(hashed_guess, hashed_password):
            x = True
    print("Password is correct")

    x = False
    while x == False:
        print("Do you want to store the password? (y/n)")
        choice = input()
        if choice == "y":
            store = [username, salt, strength, hashed_password]

            dir = (Path(__file__).resolve().parent).parent / "Data" / "Storage.txt"
            appending = '|'.join(map(str, store))
            with open(dir, "a") as file:
                file.write(appending + "\n")
            x = True

        elif choice == "n":
            print("Password not stored")
            x = True

        else:
            print("Invalid choice")

    

running = True
x = False
while x == False:
    sign_or_log = input("Do you want to sign up or log in? (sign/log):  ")

    if sign_or_log == "sign":
        write()
    elif sign_or_log == "log":
        read()