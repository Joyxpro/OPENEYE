import os
import shutil
import threading
import tkinter as tk
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import queue

current_popup = None
notification_queue = queue.Queue()
notification_in_progress = False  # Flag to track if a notification is being processed


# Define the move_explicit_image function
def move_explicit_image():
    global action_counter

    if action_counter == 0:
        return  # Do nothing if the action counter has reached zero

    # Path to the Pictures folder
    pictures_path = os.path.expanduser("~\\Pictures")

    # Path to the image named "explicit image.jpg"
    explicit_image_path = os.path.join(pictures_path, "explicit image.jpg")

    # Path to the Desktop
    desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

    # Path to the "private folder" on the Desktop
    private_folder_path = os.path.join(desktop_path, "private folder")

    # Check if the "private folder" exists, create it if it doesn't
    if not os.path.exists(private_folder_path):
        os.makedirs(private_folder_path)

    # Move the explicit image to the "private folder" if it exists
    if os.path.exists(explicit_image_path):
        shutil.move(
            explicit_image_path, os.path.join(private_folder_path, "explicit image.jpg")
        )
        print("Explicit image moved to private folder.")
        action_counter -= 1
    else:
        print("Explicit image not found.")


def disable_close():
    pass


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_delete_popup():
    global current_popup, notification_in_progress
    if current_popup is not None:
        current_popup.destroy()
    current_popup = None

    popup = tk.Toplevel()
    popup.title("Deleted")
    popup.geometry("300x150")
    popup.resizable(False, False)
    popup.attributes("-topmost", True)  # Bring to front and focus
    popup.iconbitmap("icon.ico")
    popup.configure(bg="#f8f9fa")

    message = "The explicit content has been deleted from your device."
    message_label = tk.Label(
        popup, text=message, font=("Helvetica", 12), bg="#f8f9fa", wraplength=250
    )
    message_label.pack(pady=20, padx=10)

    ok_button = tk.Button(
        popup,
        text="OK",
        font=("Helvetica", 10),
        bg="#007bff",
        fg="white",
        width=10,
        command=popup.destroy,
    )
    ok_button.pack(pady=10)

    center_window(popup)
    current_popup = popup
    notification_in_progress = False 


def show_save_popup():
    global current_popup, notification_in_progress
    if current_popup is not None:
        current_popup.destroy()
    current_popup = None

    # Create the private folder on the desktop
    desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    private_folder_path = os.path.join(desktop_path, "private folder")
    if not os.path.exists(private_folder_path):
        os.makedirs(private_folder_path)

    # Move explicit image to the private folder
    pictures_path = os.path.expanduser("~\\Pictures")
    explicit_image_path = os.path.join(pictures_path, "explicit image.jpg")
    if os.path.exists(explicit_image_path):
        shutil.move(
            explicit_image_path, os.path.join(private_folder_path, "explicit image.jpg")
        )

    popup = tk.Toplevel()
    popup.title("Saved")
    popup.geometry("300x150")
    popup.resizable(False, False)
    popup.attributes("-topmost", True)  # Bring to front and focus
    popup.iconbitmap("icon.ico")
    popup.configure(bg="#f8f9fa")

    message = "The content has been saved on your device."
    message_label = tk.Label(
        popup, text=message, font=("Helvetica", 12), bg="#f8f9fa", wraplength=250
    )
    message_label.pack(pady=20, padx=10)

    ok_button = tk.Button(
        popup,
        text="OK",
        font=("Helvetica", 10),
        bg="#007bff",
        fg="white",
        width=10,
        command=popup.destroy,
    )
    ok_button.pack(pady=10)

    center_window(popup)
    current_popup = popup
    notification_in_progress = False  # Reset the flag


def on_button_click(action):
    global current_popup, notification_in_progress
    if current_popup is not None:
        current_popup.destroy()  # Close the current notification window
    if action == "Delete":
        show_delete_popup()
    elif action == "Save":
        show_save_popup()
    print(f"Action: {action}")


def show_notification():
    global current_popup, notification_in_progress
    if notification_in_progress:
        return  # Skip processing if a notification is already being processed

    if current_popup is not None:
        current_popup.destroy()
    current_popup = None

    popup = tk.Toplevel()
    popup.title("OPENEYE Alert")
    popup.geometry("400x200")
    popup.resizable(False, False)
    popup.protocol("WM_DELETE_WINDOW", disable_close)  # Disable the close button
    popup.attributes("-topmost", True)  # Bring to front and focus
    popup.configure(bg="#f8f9fa")

    try:
        popup.iconbitmap("icon.ico")
    except Exception as e:
        print(f"Error setting icon: {e}")

    title_frame = tk.Frame(popup, bg="#f8f9fa")
    title_frame.pack(pady=10)

    img = Image.open(
        "C:\\Users\\JOY SENGUPTA\\Desktop\\code playground\\OPENEYE\\icon.ico"
    )
    img = img.resize((30, 30))
    photo = ImageTk.PhotoImage(img)

    img_label = tk.Label(title_frame, image=photo, bg="#f8f9fa")
    img_label.image = photo  # Keep a reference to the image
    img_label.pack(side="left", padx=10)

    title_label = tk.Label(
        title_frame, text="OPENEYE Alert", font=("Helvetica", 16, "bold"), bg="#f8f9fa"
    )
    title_label.pack(side="left")

    message = "OPENEYE has detected some explicit content.\nDo you want to remove it or save it?"
    message_label = tk.Label(
        popup, text=message, font=("Helvetica", 12), bg="#f8f9fa", wraplength=350
    )
    message_label.pack(pady=10, padx=10)

    button_frame = tk.Frame(popup, bg="#f8f9fa")
    button_frame.pack(pady=20)

    save_button = tk.Button(
        button_frame,
        text="Save",
        font=("Helvetica", 10),
        bg="#007bff",
        fg="white",
        width=10,
        command=lambda: on_button_click("Save"),
    )
    save_button.grid(row=0, column=0, padx=10)

    delete_button = tk.Button(
        button_frame,
        text="Delete",
        font=("Helvetica", 10),
        bg="#dc3545",
        fg="white",
        width=10,
        command=lambda: on_button_click("Delete"),
    )
    delete_button.grid(row=0, column=1, padx=10)

    center_window(popup)
    current_popup = popup
    notification_in_progress = True  # Set the flag


def process_queue():
    global notification_in_progress
    try:
        while True:
            notification_queue.get_nowait()
            if (
                not notification_in_progress
            ):  # Process if no other notification is in progress
                show_notification()
    except queue.Empty:
        pass
    root.after(100, process_queue)


class PicturesFolderHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            notification_queue.put(event)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    pictures_path = os.path.expanduser("~\\Pictures")

    event_handler = PicturesFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, path=pictures_path, recursive=True)

    print(f"Monitoring {pictures_path} for changes...")
    observer.start()

    root.after(100, process_queue)
    root.mainloop()

    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
