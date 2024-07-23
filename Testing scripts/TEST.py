import os
import shutil
from cryptography.fernet import Fernet
import getpass


# Function to generate a key and save it
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


# Function to load the key
def load_key():
    return open("key.key", "rb").read()


# Encrypt a file
def encrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)


# Decrypt a file
def decrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)


# Function to create a folder if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


# Function to delete folder contents
def delete_folder_contents(folder_name):
    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


# Main function
def main():
    folder_name = "private_folder"
    create_folder(folder_name)

    # Generate key if not exists
    if not os.path.exists("key.key"):
        generate_key()

    key = load_key()

    password = "my_secret_password"  # Set your password here
    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        entered_password = getpass.getpass("Enter password to access the folder: ")
        if entered_password == password:
            print("Access granted!")
            for filename in os.listdir(folder_name):
                file_path = os.path.join(folder_name, filename)
                decrypt_file(file_path, key)
            break
        else:
            print("Incorrect password!")
            attempts += 1

    if attempts == max_attempts:
        print("Maximum attempts reached. Deleting folder contents.")
        delete_folder_contents(folder_name)


if __name__ == "__main__":
    main()
