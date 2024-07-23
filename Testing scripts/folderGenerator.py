import os
import getpass
import shutil


def create_folder(folder_path):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Folder '{folder_path}' created.")


def lock_folder(folder_path):
    if os.path.exists(folder_path):
        # Encrypt the folder by copying its contents to a .zip file and deleting the original folder
        shutil.make_archive(folder_path, "zip", folder_path)
        shutil.rmtree(folder_path)
        print(
            f"Folder '{folder_path}' is now locked and archived as '{folder_path}.zip'."
        )
    else:
        print(f"Folder '{folder_path}' does not exist.")


def unlock_folder(folder_path, correct_password):
    # Prompt for password
    password = getpass.getpass("Enter the password to unlock the folder: ")

    if password == correct_password:
        zip_file_path = f"{folder_path}.zip"
        if os.path.exists(zip_file_path):
            shutil.unpack_archive(zip_file_path, folder_path)
            os.remove(zip_file_path)
            print(f"Folder '{folder_path}' is now unlocked.")
        else:
            print(f"Encrypted archive '{zip_file_path}' does not exist.")
    else:
        print("Incorrect password. Access denied.")


def main():
    # Get the current user's desktop path
    desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    folder_name = "private folder"
    folder_path = os.path.join(desktop_path, folder_name)
    correct_password = "your_password"  # Set your password here

    if not os.path.exists(folder_path) and not os.path.exists(f"{folder_path}.zip"):
        # If neither the folder nor the zip file exists, create the folder
        create_folder(folder_path)
    elif os.path.exists(folder_path):
        # If the folder exists, lock it
        lock_folder(folder_path)
    else:
        # If the zip file exists, unlock the folder
        unlock_folder(folder_path, correct_password)


if __name__ == "__main__":
    main()
