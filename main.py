from functions import *
import os 
os.system("cls")
phonebook = load_contacts()

menu = {
    "1": add_contact,
    "2": show_contacts,
    "3": search_contact,
    "4": sort_contacts
}

while True:
    print("\nPHONEBOOK")
    for key in menu:
        print(f"{key}. {menu[key].__name__.replace('_', ' ').title()}")
    print("5. Exit")

    choice = input("Choose an option: ")
    os.system("cls")

    if choice in menu:
        menu[choice](phonebook)

    elif choice == "5":
        save_contacts(phonebook)
        print("Program exiting.")
        break

    else:
        print("Invalid choice.")