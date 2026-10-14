from pathlib import Path

dir = Path(__file__).resolve().parent

dir = dir.parent / "Data" / "Storage.txt"

store = ["name", "3", "hha", "9swhshdf"]

appending = "|".join(store)

with open(dir, "a") as file:
    file.write("\n" + appending)