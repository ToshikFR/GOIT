from datetime import datetime, timedelta
import pickle
from pathlib import Path
from test import FileSorter
from abc import ABC, abstractmethod

class Contact:
    def __init__(self, name, address, phone, email, birthday):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday

class Note:
    def __init__(self, text):
        self.text = text
        self.tags = []

class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_notes(self, notes):
        pass

    @abstractmethod
    def display_menu(self):
        pass

    @abstractmethod
    def get_user_input(self, prompt):
        pass

class ConsoleInterface(UserInterface):
    def display_contacts(self, contacts):
        print("Contacts:")
        for contact in contacts:
            print(f"{contact.name} | {contact.address} | {contact.phone} | {contact.email} | {contact.birthday}")

    def display_notes(self, notes):
        print("Notes:")
        for note in notes:
            print(f"{note.title} | {note.text} | {', '.join(note.tags)}")

    def display_message(self, message):
        print(message)

    def display_menu(self):
        print("\nI can perform the following commands:")
        print("1 - Add contact")
        print("2 - Search contacts")
        print("3 - Delete contact")
        print("4 - Edit contact")
        print("5 - Find upcoming birthdays")
        print("6 - Add note")
        print("7 - Search note")
        print("8 - Edit or delete note")
        print("9 - Add tags to note")
        print("10 - Search notes by tags")
        print("sort - Sort folder")
        print("save - Save data")
        print("load - Load data")
        print("menu - Display menu")
        print("end, close, exit - Exit program")

    def get_user_input(self, prompt):
        return input(prompt)

class BotAssist:
    def __init__(self, user_interface):
        self.contacts = []
        self.notes = {}
        self.tags = {}
        self.user_interface = user_interface

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10

    def validate_email(self, email):
        return '@' in email and '.' in email.split('@')[-1]

    def add_contact(self, name, address, phone, email, birthday):
        if not self.validate_phone(phone):
            print("Invalid phone number format. Please enter a 10-digit number.")
            return

        if not self.validate_email(email):
            print("Invalid email format. Please enter a valid email address.")
            return
        
        for contact in self.contacts:
          if contact.name.lower() == name.lower() and contact.birthday.lower() == birthday.lower():
             print(f"Contact with name '{name}' and birthday '{birthday}' already exists. Can not duplicate contact.")
             return

        contact = Contact(name, address, phone, email, birthday)
        self.contacts.append(contact)
        print("Contact added successfully.")
        
    def search_contacts_birthday(self, days):
        upcoming_birthday_contacts = []
        today = datetime.now()

        for contact in self.contacts:
            birthday_month, birthday_day = map(int, contact.birthday.split('-')[1:])
            birthday_date = datetime(today.year, birthday_month, birthday_day)

        
            if birthday_date < today:
            
                birthday_date = datetime(today.year + 1, birthday_month, birthday_day)

            days_until_birthday = (birthday_date - today).days

            if -1 <= days_until_birthday <= days:
                upcoming_birthday_contacts.append(contact)

        if upcoming_birthday_contacts:
            print("Contacts with upcoming birthdays:")
            for contact in upcoming_birthday_contacts:
                print(contact.name, "|", contact.address, "|", contact.phone, "|", contact.email, "|", contact.birthday, "|")
        else:
            print("No contacts with upcoming birthdays.")

    


    def search_contacts(self, query):
        results = []
        for contact in self.contacts:
            if query.lower() in contact.name.lower():
                results.append(contact)
        return results
     

    def edit_contact(self, old_contact_name, new_name, new_address, new_phone, new_email, new_birthday):
      contact_found = False
      if not self.validate_phone(new_phone):
        print("Invalid phone number format. Please enter a 10-digit number.")
        return

      if not self.validate_email(new_email):
        print("Invalid email format. Please enter a valid email address.")
        return
      for contact in self.contacts:
        if contact.name.lower() == old_contact_name.lower():
            contact_found = True
            contact.name = new_name
            if not new_address==None:
                contact.address = new_address
            contact.phone = new_phone
            contact.email = new_email
            if not new_birthday==None:
                contact.birthday = new_birthday
            break

      if not contact_found:
         return f'Contact not found'

      return f'Contact {old_contact_name} successfully edited.'


    def delete_contact(self, contact_name):

        for contact in self.contacts:
            if contact_name.lower() in contact.name.lower():
                self.contacts.remove(contact)
                print(f'{contact_name} removed')
            else:
                print("Contact not found")
                
                
    
      

    def add_note(self, note_name, note_text):
        if note_name in self.notes:  # Перевірка, чи назва нотатки вже існує
            choice = input(f"Note '{note_name}' already exists. Do you want to edit it? enter yes or no: ").lower()
            if choice == 'yes':
                self.edit_note(note_name, note_text)  # Виклик методу для редагування нотатки
            else:
                print("Note creation aborted.")
        else:
            self.notes[note_name] = Note(note_text)  # Створення нової нотатки в словнику notes
            print(f"Note '{note_name}' created successfully.")

    def search_notes(self, note_name):
        if not self.notes:  # Перевірка, чи словник notes пустий
            print("Notes not found. Please create a note using command '6'.")
        elif note_name in self.notes:  # Пошук нотатки за вказаною назвою
            print(f"Note '{note_name}': {self.notes[note_name].text}")
        else:
            print(f"Note '{note_name}' does not exist.")

    def edit_note(self, note_name, new_text):
        if note_name in self.notes:  # Перевірка, чи існує нотатка з вказаною назвою
            self.notes[note_name].text = new_text  # Зміна тексту нотатки
            print(f"Edited note '{note_name}' successfully.")
        else:
            print(f"Note '{note_name}' does not exist. Cannot edit.")

    def delete_note(self, note_name):
        if not self.notes:  # Перевірка, чи словник notes пустий
            print("No notes found. Please create a note using command '6'.")
        elif note_name in self.notes:  # Перевірка, чи існує нотатка з вказаною назвою
            print(f"Note '{note_name}': {self.notes[note_name].text}")
            choice = input(f"Are you sure you want to delete note '{note_name}'? (1 - Yes, 2 - No): ")
            if choice == '1':
                del self.notes[note_name]  # Видалення нотатки за вказаною назвою
                print(f"Note '{note_name}' deleted successfully.")
            else:
                print("Deletion aborted.")
        else:
            print(f"Note '{note_name}' does not exist.")
            
            
    def add_tags_to_note(self, title, new_tags):
        if title in self.notes:
            self.notes[title].tags.extend(new_tags)
            for tag in new_tags:
                if tag in self.tags:
                    self.tags[tag].append(title)
                else:
                    self.tags[tag] = [title]
            print("Tags added successfully.")
        else:
            print("Note not found.")
            
    def search_notes_by_tags(self, tags):
        results = []
        for note_name, note in self.notes.items():
            if all(tag in note.tags for tag in tags):
                results.append(note)
        sorted_results = sorted(results, key=lambda x: x.text)
        return sorted_results


    def save_data(self, filename):
        with open(filename, "wb") as file:
            data = (self.contacts, self.notes, self.tags)
            pickle.dump(data, file)
        print("Data saved successfully.")

    def load_data(self, filename):
        try:
            with open(filename, 'rb') as file:
                data = pickle.load(file)
                self.contacts = data.get(self.contacts)
                self.notes = data.get(self.notes)
                self.tags = data.get(self.tags)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("File not found. No data loaded.")

    def sort_files(self, folder_path):
        file_sorter = FileSorter(folder_path)
        file_sorter.core()

    def display_contacts(self):
        self.user_interface.display_contacts(self.contacts)

    def display_notes(self):
        self.user_interface.display_notes(self.notes.values())

    def display_menu(self):
        self.user_interface.display_menu()

    def get_user_input(self, prompt):
        return self.user_interface.get_user_input(prompt)

def main():
   console_interface = ConsoleInterface()
   assistant = BotAssist(console_interface)

   while True:
       command = input("\nEnter your command for start(for menu-press 'menu'): ").lower()
    
       if command == '1':
            
            name = console_interface.get_user_input('Enter your name:')
            address = console_interface.get_user_input('Enter your address:')
            phone = console_interface.get_user_input('Enter your phone:')
            email = console_interface.get_user_input('Enter your email:')
            birthday = console_interface.get_user_input('Enter your birthday:')
            

            assistant.add_contact(name, address, phone, email, birthday)

       elif command == '2':  
            search_query = console_interface.get_user_input("Enter first name or last name: ")
            results = assistant.search_contacts(search_query)
            if results:
                print("Search Results:")
                for result in results:
                    print(result.name, "|", result.address, "|", result.phone, "|", result.email, "|", result.birthday, "|")
            else:
                print("No contacts found.")

       elif command == '3':
            contact_name = console_interface.get_user_input('Enter the contact name you want to delete:')
            assistant.delete_contact(contact_name)

       elif command == '4':
            old_contact_name = console_interface.get_user_input('Enter the contact old name you want to edit: ')
            new_name = console_interface.get_user_input('Enter the new name: ')
            new_address = console_interface.get_user_input('Enter the new address: ')
            new_phone = console_interface.get_user_input('Enter the new phone: ')
            new_email = console_interface.get_user_input('Enter the new email: ')
            new_birthday = console_interface.get_user_input('Enter the new birthday in YYYY-MM-DD: ')
            print(assistant.edit_contact(old_contact_name, new_name, new_address, new_phone, new_email, new_birthday))

       elif command == '5':
            day_to_birthday = int(console_interface.get_user_input("Enter the number of days until the birthday: "))
            assistant.search_contacts_birthday(day_to_birthday)

       elif command == '6':
            note_name = console_interface.get_user_input("Enter note name: ")
            note_text = console_interface.get_user_input("Enter note text: ")
            assistant.add_note(note_name, note_text)

       elif command == '7':
            note_name = console_interface.get_user_input("Enter note name to search: ")
            assistant.search_notes(note_name)

       elif command == '8':
            edit_or_delete = console_interface.get_user_input("Enter 'edit' to edit a note or 'delete' to delete a note: ").lower()

            if edit_or_delete == 'edit':
                note_name = console_interface.get_user_input("Enter note name to edit: ")
                new_text = console_interface.get_user_input("Enter new text for the note: ")
                assistant.edit_note(note_name, new_text)
            elif edit_or_delete == 'delete':
                note_name = console_interface.get_user_input("Enter note name to delete: ")
                assistant.delete_note(note_name)
            else:
                console_interface.display_message("Invalid command. Please enter 'edit' or 'delete'.")

       elif command == '9':
            title = console_interface.get_user_input("Enter note name:")
            new_tags = console_interface.get_user_input("Enter tags (comma separated):").split(",")
            assistant.add_tags_to_note(title, new_tags)

       elif command == '10':
            tags = console_interface.get_user_input("Enter tags for search (comma separated):").split(",")
            results = assistant.search_notes_by_tags(tags)
            if results:
                for result in results:
                    console_interface.display_message(f"{result.tags} | {result.text}")
            else:
                console_interface.display_message("Not found.")

       elif command == 'sort':
            folder_path = console_interface.get_user_input("Enter the folder path to sort :")
            assistant.sort_files(folder_path)
            console_interface.display_message("Folder is sorted successfully!")

       elif command == 'save':
            filename = console_interface.get_user_input("Enter the filename to save data: ")
            assistant.save_data(filename)
            console_interface.display_message("Data saved successfully.")

       elif command == 'load':
            filename = console_interface.get_user_input("Enter the filename to load data: ")
            assistant.load_data(filename)
            console_interface.display_message("Data loaded successfully.")

       elif command == 'menu':
            console_interface.display_menu()

       elif command in ['exit', 'end', 'close']:
            console_interface.display_message("Closing. Bye")
            break
       else:
            console_interface.display_message("Invalid command. Try again.")
   return assistant
           
if __name__ == "__main__":
    main()