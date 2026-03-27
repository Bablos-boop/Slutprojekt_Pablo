import csv
import os 

FILENAME = "contacts.csv"

def load_contacts():
    phonebook = []
    try:
        with open(FILENAME, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get("name") or row.get(" name")
                number = row.get("number") or row.get(" number")
                if name and number:
                    phonebook.append({"name": name.strip(), "number": number.strip()})
    except FileNotFoundError:
        pass
    return phonebook


def save_contacts(phonebook):
    try:
        with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "number"])
            writer.writeheader()
            writer.writerows(phonebook)
    except Exception as e:
        print(f"Fel vid sparning: {e}")



def add_contact(phonebook):
    name = input("Enter name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    
    while True:
        try:
            number_input = input("Enter number: ").strip()
            if not number_input:
                print("Number cannot be empty.")
                continue
            number = int(number_input)
            break
        except ValueError:
            print("Please enter a valid number.")
    
    contact = {"name": name, "number": number}
    phonebook.append(contact)
    save_contacts(phonebook)
    print("Contact added!")
    
def show_contacts(phonebook):
    if len(phonebook) == 0:
        print("Phonebook is empty.")
    else: 
        for contact in phonebook:
            print(f"Name: {contact['name']}, Number: {contact['number']}")
            input("Press Anything to Continue")
            
def search_contact(phonebook):
    search = input("Search for name: ")

    found = False
    for contact in phonebook:
        if contact["name"].lower() == search.lower():
            print(f"Found: {contact['name']} - {contact['number']}")
            found = True
            
    if not found:
        os.system("cls")
        print("No contact found.")
        
def sort_contacts(phonebook):
    phonebook.sort(key=lambda contact: contact["name"].lower())
    save_contacts(phonebook)
    print("Contacts sorted by name.")