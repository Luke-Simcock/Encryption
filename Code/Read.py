#Importations
from pathlib import Path

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
    print("Username found")

else:
    print("Username not found.")

exit()