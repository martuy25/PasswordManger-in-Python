import getpass
import secrets
import string

class PasswordManager:
    def __init__(self):
        self.passwords = {} #dictionary to store account password pairs
        
    def menu(self):
        while True:
            print("\nPassword Manager Menu: ")
            print('1. Add Password')
            print("2. Retrieve Password")
            print("3. Exit")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.add_password()
            elif choice == "2":
                self.retrieve_password()
            elif choice == "3":
                print("Existing Password Manager.")
                break
            else:
                print("Invaid choice. Please Try again.")
    
    def generate_password(self,length=12):
        characters = string.ascii_letters+ string.digits + string.punctuation
        password = ''.join(secrets.choice(characters)for i in range(length))
        return password            
    
    def add_password(self):
        account = input('Enter the account name: ')
        password = self.generate_password()
        self.passwords[account] = password
        print("Password added succesfully.")
        
    def retrieve_password(self):
        account = input("Enter the account name: ")
        if account in self.passwords:
            print("Password: ", self.passwords[account])
        else: 
            print("account not found")
    
            
if __name__ == "__main__":
    manager = PasswordManager()
    manager.menu()
                
            