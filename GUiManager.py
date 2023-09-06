import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import sqlite3

#creating the main window
window = tk.Tk()
window.title("Password Manager")

#Creating labels, entry fields and buttons
label_account = tk.Label(window, text="Account")
entry_account = tk.Entry(window)
label_password = tk.Label(window, text="Password")
entry_password = tk.Entry(window, show="*")
button_save = tk.Button(window, text="Save Password")
button_show = tk.Button(window, text="Show Password")


# Creating the Grid layout
label_account.grid(row=0, column=0)
entry_account.grid(row=0, column=1)
label_password.grid(row=1, column=0)
entry_password.grid(row=1, column=1)
button_save.grid(row=2, column=0)
button_show.grid(row=2, column=1)

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

def encrypt(password):
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt(encrypted_password):
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password


#creating the function to save the passwords
def save_password():
    account = entry_account.get()
    password = entry_password.get()
    encrypt_password = encrypt(password)
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (account, password) VALUES(?, ?)", (account, encrypt_password))
    conn.commit()
    conn.close()
    entry_account.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    messagebox.showinfo("Success", "Password saved succesfully")
    
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

# Start the GUI
window.mainloop()
    
