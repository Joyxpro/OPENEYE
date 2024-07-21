import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from win10toast import ToastNotifier


class PicturesFolderHandler(FileSystemEventHandler):
    def __init__(self):
        self.toaster = ToastNotifier()
        super().__init__()

    def on_any_event(self, event):
        if not event.is_directory:
            self.toaster.show_toast(
                "Notification", "Pictures folder has been accessed!", duration=10
            )


if __name__ == "__main__":
    pictures_path = os.path.expanduser("~\\Pictures")

    event_handler = PicturesFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, path=pictures_path, recursive=True)

    print(f"Monitoring {pictures_path} for changes...")
    observer.start()

    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
