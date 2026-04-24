import csv
import os 

FILENAME = "contacts.csv"

def load_contacts():
    # Laddar kontakter från CSV-fil
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
    # Sparar kontakter till CSV-fil
    try:
        with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "number"])
            writer.writeheader()
            writer.writerows(phonebook)
    except Exception as e:
        print(f"Fel vid sparning: {e}")



def add_contact(phonebook):
    # Lägger till ny kontakt i listan
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
            os.system("cls")
            print("Please enter a valid number.")
    
    contact = {"name": name, "number": number}
    phonebook.append(contact)
    save_contacts(phonebook)
    print("Contact added!")
    
def show_contacts(phonebook):
    # Visar alla kontakter i listan
    if len(phonebook) == 0:
        print("Phonebook is empty.")
    else: 
        for contact in phonebook:
            
            print(f"Name: {contact['name']}, Number: {contact['number']}")
            
            
            
def search_contact(phonebook):
    # Söker efter matchande kontakt
    search = input("Search for name: ")

    found = False
    os.system("cls")
    for contact in phonebook:
       if search.lower() in contact ["name"].lower():
            print(f"Found: {contact['name']} - {contact['number']}")
            found = True
            
            
    if not found:
        print("No contact found.")
        
def sort_contacts(phonebook):
    # Sorterar kontakter efter namn eller nummer
    print("How do you want it sorted?")
    print("1. Name (A-Z)")
    print("2. Name(Z-A)")
    print("3. Phone number")
    
    try:
        choice_sort = int(input("Choose an option"))
    except ValueError:
        print("Invalid Error")
        return 
    if choice_sort == 1:
        phonebook.sort(key=lambda contact: contact["name"].lower())
    elif choice_sort == 2:
        phonebook.sort(key=lambda contact: contact["name"].lower(), reverse=True)
    elif choice_sort == 3:
        phonebook.sort(key=lambda contact: contact["number"])       
        
    else: 
        print("No")
        return
    save_contacts(phonebook)
    print("Contacts sorted by name.")


def delete_contact(phonebook):
    # Raderar kontakt med matchande bokstäver
    search = input("Search for name: ").strip()

    
    os.system("cls")
    for contact in phonebook:
       if search.lower() in contact ["name"].lower():
            phonebook[:] = [c for c in phonebook if search.lower() not in c["name"].lower()]
            print(f"Deleting: {contact['name']} - {contact['number']}")
            save_contacts(phonebook)
            found = True
            
      
def update_contact(phonebook):
    # Ändrar befintlig kontakts namn och nummer
    search = input("Vem vill du ändra? (Ange namn): ").strip()
    found_contacts = []

    # 1. Hitta alla matchningar (likt din sökfunktion)
    for contact in phonebook:
        if search.lower() in contact["name"].lower():
            found_contacts.append(contact)

    if not found_contacts:
        print("Hittade ingen kontakt med det namnet.")
        return

    # 2. Om det finns flera matchningar, låt användaren välja
    print("\nHittade följande kontakter:")
    for i, contact in enumerate(found_contacts, 1):
        print(f"{i}. {contact['name']} - {contact['number']}")

    try:
        choice = int(input("\nVilken vill du ändra? (Ange siffra, eller 0 för att avbryta): "))
        if choice == 0:
            return
        target = found_contacts[choice - 1]
    except (ValueError, IndexError):
        print("Ogiltigt val.")
        return

    # 3. Fråga efter nya uppgifter (lämna tomt för att behålla gamla)
    print(f"\nRedigerar {target['name']}. Lämna tomt för att behålla nuvarande värde.")
    
    new_name = input(f"Nytt namn [{target['name']}]: ").strip()
    if new_name:
        target['name'] = new_name

    while True:
        new_number = input(f"Nytt nummer [{target['number']}]: ").strip()
        if not new_number:
            # Användaren tryckte bara Enter, behåll gamla numret
            break
        try:
            target['number'] = int(new_number)
            break
        except ValueError:
            print("Vänligen ange ett giltigt nummer (bara siffror).")

    # 4. Spara ändringarna till filen
    save_contacts(phonebook)
    print("Kontakten har uppdaterats!")