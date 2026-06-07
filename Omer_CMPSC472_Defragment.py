import math

MAX_SECTORS = 40
SECTOR_SIZE = 500

# initialize sectors
sectors = ['-'] * MAX_SECTORS

# file tracking table
files = {}

# hard-coded fragmented layout
initial_layout = [
'A','B','B','-','D','-','X','X','-','E','F','G','-','H','H','J','J','-','-','J',
'K','K','J','L','L','L','-','M','M','P','P','M','P','P','-','-','R','-','-','-'
]

for i in range(len(initial_layout)):
    sectors[i] = initial_layout[i]

# build tracking table
def rebuild_tracking():
    files.clear()
    for i in range(MAX_SECTORS):
        name = sectors[i]
        if name != '-':
            if name not in files:
                files[name] = {"sectors": [], "size": 0}
            files[name]["sectors"].append(i)
            files[name]["size"] = len(files[name]["sectors"]) * SECTOR_SIZE


def display_sectors():
    print("\nSector Map")
    print("---------------------------")
    for i in range(MAX_SECTORS):
        print(f"{i:2} : {sectors[i]}")
    print()


def display_files():
    print("\nFile Tracking Table")
    print("---------------------------------------")
    print("File   StartSector   Size(bytes)")
    for name in files:
        start = files[name]["sectors"][0]
        size = files[name]["size"]
        print(f"{name:4}   {start:10}   {size}")
    print()


def add_file():
    name = input("Enter file name: ").upper()

    if name in files:
        print("File already exists.")
        return

    size = int(input("Enter file size in bytes: "))
    sectors_needed = math.ceil(size / SECTOR_SIZE)

    empty = []
    for i in range(MAX_SECTORS):
        if sectors[i] == '-':
            empty.append(i)

    if len(empty) < sectors_needed:
        print("Not enough space.")
        return

    used = empty[:sectors_needed]

    for i in used:
        sectors[i] = name

    rebuild_tracking()
    print("File added.")


def remove_file():
    name = input("Enter file name to remove: ").upper()

    if name not in files:
        print("File not found.")
        return

    for i in files[name]["sectors"]:
        sectors[i] = '-'

    rebuild_tracking()
    print("File removed.")


def defragment():
    swaps = 0
    write_index = 0

    for read_index in range(MAX_SECTORS):
        if sectors[read_index] != '-':
            if read_index != write_index:
                sectors[write_index], sectors[read_index] = sectors[read_index], sectors[write_index]
                swaps += 1
            write_index += 1

    rebuild_tracking()

    print("\nDefragmentation complete.")
    print("Sector swaps:", swaps)


def menu():
    while True:
        print("\n1. Add File")
        print("2. Remove File")
        print("3. Defragment")
        print("4. Display Sectors")
        print("5. Display File Table")
        print("6. Exit")

        choice = input("Choose option: ")

        if choice == '1':
            add_file()
        elif choice == '2':
            remove_file()
        elif choice == '3':
            defragment()
        elif choice == '4':
            display_sectors()
        elif choice == '5':
            display_files()
        elif choice == '6':
            break
        else:
            print("Invalid option")


def main():
    print("Welcome to Hard Drive Defragmentation Simulator")
    print("This program simulates organizing fragmented disk sectors.\n")

    rebuild_tracking()

    print("BEFORE Defragmentation:")
    display_sectors()

    menu()

    print("\nFinal Sector Layout:")
    display_sectors()
    display_files()


main()