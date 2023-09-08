import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import sqlite3
import os
import secrets
import string

#creating the main window
window = tk.Tk()
window.title("Password Manager")

#Create golbal database
conn = None

#Creating labels, entry fields and buttons
label_account = tk.Label(window, text="Account")
entry_account = tk.Entry(window)
label_password = tk.Label(window, text="Password")
entry_password = tk.Entry(window, show="*")
button_save = tk.Button(window, text="Save Password")
button_show = tk.Button(window, text="Show Password")
button_generate_password = tk.Button(window, text="Generate Password")
label_password_strength = tk.Label(window, text="Password Strength:")
button_check_password = tk.Button(window, text="Check Password Strength")
entry_check_password = tk.Entry(window, show="*")
button_update_password = tk.Button(window, text="Update Password")
button_delete_password = tk.Button(window, text="Delete Password")


# Creating the Grid layout
label_account.grid(row=0, column=0)
entry_account.grid(row=0, column=1)
label_password.grid(row=1, column=0)
entry_password.grid(row=1, column=1)
button_save.grid(row=2, column=0)
button_show.grid(row=2, column=1)
button_generate_password.grid(row=3, column=0, columnspan=2)
label_password_strength.grid(row=5, column=0, columnspan=2)
button_check_password.grid(row=7, column=0, columnspan=2)
entry_check_password.grid(row=6, column=0, columnspan=2)
button_update_password.grid(row=8, column=0)
button_delete_password.grid(row=8, column=1)



#Generate a key and storing securely
#define key path
key_file_path = "secret.key"


#check to see if key file exist
if os.path.isfile(key_file_path):
    #load key from file if available
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
else:
    #generate key if none found
    key = Fernet.generate_key()
    with open(key_file_path, "wb")as key_file:
        key_file.write(key)

#cipher_key
cipher_suite = Fernet(key)

# Encrypt and decrypt functions
def encrypt(password):
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt(encrypted_password):
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

def generate_complex_password():
    #defining character sets
    letters = string.ascii_letters
    num = string.digits
    special_characters = string.punctuation
    
    complexPass = (secrets.choice(letters) + secrets.choice(num) + secrets.choice(special_characters) +
        ''.join(secrets.choice(letters+num+special_characters) for i in range(12))
    )    
    entry_password.delete(0, tk.END)
    entry_password.insert(0, complexPass)
        
def check_password_strength(password):
    length_check = len(password) >= 8
    uppercase_check = any(check.isupper() for check in password)
    lowercase_check = any(check.islower() for check in password)
    num_check = any(check.isdigit() for check in password)
    special_check = any(check in string.punctuation for check in password)
    
   #calculate password strength
    strength_score = sum([length_check, uppercase_check, lowercase_check, num_check, special_check])
    # Display score
    strength_labels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    password_strength = strength_labels[strength_score]
    label_password_strength.config(text="Password Strength: " + password_strength)


#creating the function to save the passwords
def save_password():
    global conn #to access the global database
    account = entry_account.get()
    password = entry_password.get()
    encrypt_password = encrypt(password)
    
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO passwords (account, password) VALUES(?, ?)", (account, encrypt_password))
        entry_account.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        messagebox.showinfo("Success", "Password saved successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Account already exists in the database")
   

# Function to update a password
def update_password():
    global conn 
    account = entry_account.get()
    new_password = entry_password.get()
    encrypt_new_password = encrypt(new_password)
    
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE passwords SET password=? WHERE account=?", (encrypt_new_password, account))
        entry_account.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        messagebox.showinfo("Success", "Password updated successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Account not found in the database")

    

# Function to delete a password
def delete_password():
    global conn
    account = entry_account.get()
    
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE account=?", (account,))
        entry_account.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        messagebox.showinfo("Success", "Password deleted successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Account not found in the database")

    
#Function to show passwords
def show_password():
    account = entry_account.get()
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM passwords WHERE account=?", (account,))
    result = cursor.fetchone()
    conn.close()
    if result:
        decrypted_password = decrypt(result[0])
        messagebox.showinfo("Password", f"Password for {account}: {decrypted_password}")
    else:
        messagebox.showerror("Error", f"Account '{account}' not found!")
    
#create the database and tables
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (account TEXT PRIMARY KEY, password TEXT)''')
conn.commit()
conn.close()

# Bind functions to buttons
button_save.config(command=save_password)
button_show.config(command=show_password)
button_generate_password.config(command=generate_complex_password)
button_check_password.config(command=lambda: check_password_strength(entry_check_password.get()))
button_update_password.config(command=update_password)
button_delete_password.config(command=delete_password)

security_explanation = """
Security Note:
The complex password generator uses the 'secrets' module, which is designed specifically for cryptographic applications and provides a higher level of security compared to the 'random' module. 'secrets' generates cryptographically secure random numbers suitable for password generation, making it extremely difficult for attackers to predict or guess generated passwords.

Additionally, the generated password includes a mix of uppercase and lowercase letters, digits, and special characters, making it more resilient against common password attacks.

Remember to store generated passwords securely and never reveal them unnecessarily. Consider using a password manager to manage and store your passwords safely.
"""

# Display the security explanation in a message box
messagebox.showinfo("Security Information", security_explanation)

conn = sqlite3.connect("passwords.db")

# Start the GUI
window.mainloop()
    
