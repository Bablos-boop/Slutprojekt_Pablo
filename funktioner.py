def add_contact(phonebook):
    name = input("Enter name: ")
    number = int(input("Enter number:"))
    
    contact = {"Name": name, "number": number}
    phonebook.append(contact)
    print("Contact added!")
    
def show_contacts(phonebook):
    if len(phonebook) == 0:
        print("Phonebook is empty.")
    else: 
        for contact in phonebook:
            print(f"Name: {contact['name']}, Number: {contact['number']}")
            
def search_contact(phonebook):
    search = input("Search for name: ")

    found = False
    for contact in phonebook:
        if contact["name"].lower() == search.lower():
            print(f"Found: {contact['name']} - {contact['number']}")
            found = True
            
    if not found:
        print("No contact found.")
        
def sort_contacts(phonebook):
    phonebook.sort(key=lambda contact: contact["name"])
    print("Contact sorted by name")