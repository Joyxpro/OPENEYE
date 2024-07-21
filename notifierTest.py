import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import queue


class OpenEyeApp:
    def __init__(self):
        self.current_popup = None
        self.notification_queue = queue.Queue()
        self.actions_remaining = 100

        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

        self.pictures_path = os.path.expanduser("~\\Pictures")
        self.desktop_path = os.path.join(
            os.path.join(os.environ["USERPROFILE"]), "Desktop"
        )
        self.private_folder_path = os.path.join(self.desktop_path, "private folder")

        self.icon_image = self.load_icon(
            "C:\\Users\\JOY SENGUPTA\\Desktop\\code playground\\OPENEYE\\icon.ico"
        )

        event_handler = PicturesFolderHandler(self.notification_queue)
        self.observer = Observer()
        self.observer.schedule(event_handler, path=self.pictures_path, recursive=True)

        print(f"Monitoring {self.pictures_path} for changes...")
        self.observer.start()

        self.root.after(100, self.process_queue)
        self.root.mainloop()

    def load_icon(self, path):
        try:
            img = Image.open(path)
            img = img.resize((30, 30))
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading icon: {e}")
            return None

    def move_explicit_image(self):
        explicit_image_path = os.path.join(self.pictures_path, "explicit image.jpg")
        if not os.path.exists(self.private_folder_path):
            os.makedirs(self.private_folder_path)

        if os.path.exists(explicit_image_path):
            shutil.move(
                explicit_image_path,
                os.path.join(self.private_folder_path, "explicit image.jpg"),
            )
            print("Explicit image moved to private folder.")
        else:
            print("Explicit image not found.")

    def delete_explicit_image(self):
        explicit_image_path = os.path.join(self.pictures_path, "explicit image.jpg")
        if os.path.exists(explicit_image_path):
            os.remove(explicit_image_path)
            print("Explicit image deleted.")
        else:
            print("Explicit image not found.")

    def disable_close(self):
        pass

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def show_popup(self, title, message, button_text, button_command):
        if self.current_popup is not None:
            self.current_popup.destroy()
        self.current_popup = None

        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.attributes("-topmost", True)  # Bring to front and focus
        popup.configure(bg="#f8f9fa")

        try:
            popup.iconbitmap("icon.ico")
        except Exception as e:
            print(f"Error setting icon: {e}")

        message_label = tk.Label(
            popup, text=message, font=("Helvetica", 12), bg="#f8f9fa", wraplength=250
        )
        message_label.pack(pady=20, padx=10)

        ok_button = tk.Button(
            popup,
            text=button_text,
            font=("Helvetica", 10),
            bg="#007bff",
            fg="white",
            width=10,
            command=lambda: self.close_popup(popup, button_command),
        )
        ok_button.pack(pady=10)

        self.center_window(popup)
        self.current_popup = popup

    def close_popup(self, popup, command):
        popup.destroy()
        if command:
            command()

    def on_button_click(self, action):
        if self.actions_remaining <= 0:
            return  # No more actions allowed

        if self.current_popup is not None:
            self.current_popup.destroy()  # Close the current notification window

        if action == "Delete":
            self.delete_explicit_image()  # Delete the image
            self.show_popup(
                "Deleted",
                "The explicit content has been deleted from your device.",
                "OK",
                None,
            )
        elif action == "Save":
            self.move_explicit_image()
            self.show_popup(
                "Saved", "The content has been saved on your device.", "OK", None
            )

        self.actions_remaining -= 1  # Decrement the counter
        print(f"Action: {action}, Actions remaining: {self.actions_remaining}")

    def show_notification(self):
        if self.current_popup is not None:
            self.current_popup.destroy()
        self.current_popup = None

        popup = tk.Toplevel()
        popup.title("OPENEYE Alert")
        popup.geometry("400x200")
        popup.resizable(False, False)
        popup.protocol(
            "WM_DELETE_WINDOW", self.disable_close
        )  # Disable the close button
        popup.attributes("-topmost", True)  # Bring to front and focus
        popup.configure(bg="#f8f9fa")

        try:
            popup.iconbitmap("icon.ico")
        except Exception as e:
            print(f"Error setting icon: {e}")

        title_frame = tk.Frame(popup, bg="#f8f9fa")
        title_frame.pack(pady=10)

        if self.icon_image:
            img_label = tk.Label(title_frame, image=self.icon_image, bg="#f8f9fa")
            img_label.pack(side="left", padx=10)

        title_label = tk.Label(
            title_frame,
            text="OPENEYE Alert",
            font=("Helvetica", 16, "bold"),
            bg="#f8f9fa",
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
            command=lambda: self.on_button_click("Save"),
        )
        save_button.grid(row=0, column=0, padx=10)

        delete_button = tk.Button(
            button_frame,
            text="Delete",
            font=("Helvetica", 10),
            bg="#dc3545",
            fg="white",
            width=10,
            command=lambda: self.on_button_click("Delete"),
        )
        delete_button.grid(row=0, column=1, padx=10)

        self.center_window(popup)
        self.current_popup = popup

    def process_queue(self):
        try:
            while True:
                self.notification_queue.get_nowait()
                if self.actions_remaining > 0:
                    self.show_notification()
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)


class PicturesFolderHandler(FileSystemEventHandler):
    def __init__(self, notification_queue):
        super().__init__()
        self.notification_queue = notification_queue

    def on_any_event(self, event):
        if not event.is_directory:
            self.notification_queue.put(event)


if __name__ == "__main__":
    try:
        app = OpenEyeApp()
    except KeyboardInterrupt:
        app.observer.stop()
        app.observer.join()
