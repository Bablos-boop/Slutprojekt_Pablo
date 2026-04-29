from functions import *
import os 
os.system("cls")
phonebook = load_contacts()

menu = {
    "1": add_contact,
    "2": show_contacts,
    "3": search_contact,
    "4": sort_contacts,
    "5": delete_contact,
    "6": update_contact,
    "7": show_categories,
    "8": show_contacts_by_category,
    "9": change_contact_category,
}

while True:
    print("\nPHONEBOOK")
    if len(phonebook) == 0:
        print("Phonebook is empty.")
    else: 
        for contact in phonebook:
            print(f"{contact['name']}, {contact['number']}")
            
    for key in menu:
        
        print(f"{key}. {menu[key].__name__.replace('_', ' ').title()}")
    print("10. Exit")

    choice = input("Choose an option: ")
    os.system("cls")

    if choice in menu:
        menu[choice](phonebook)

    elif choice == "10":
        save_contacts(phonebook)
        print("Program exiting.")
        break

    else:
        print("Invalid choice.")