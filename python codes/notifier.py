import tkinter as tk
from tkinter import ttk, messagebox


def on_block():
    # Display the confirmation popup
    messagebox.showinfo(
        "Action", "The content has been blocked from further surfacing."
    )
    root.destroy()


def on_keep():
    # Display the confirmation popup
    messagebox.showinfo("Action", "The content will continue to surface.")
    root.destroy()


root = tk.Tk()
root.title("OPENEYE Alert")

# Disable the close button (X)
root.protocol("WM_DELETE_WINDOW", lambda: None)

# Increase the size of the popup box
popup_width = 600
popup_height = 250

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the popup
center_x = int(screen_width / 2 - popup_width / 2)
center_y = int(screen_height / 2 - popup_height / 2)

# Set the geometry of the window
root.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")

# Apply a modern theme
style = ttk.Style(root)
style.theme_use("clam")  # Use 'clam' theme for a modern look

# Customize styles
style.configure("TLabel", font=("Helvetica", 12), padding=10, background="#f0f0f0")
style.configure(
    "TButton",
    font=("Helvetica", 12),
    padding=5,
    background="#007bff",
    foreground="white",
    borderwidth=0,
)
style.map(
    "TButton",
    background=[("active", "#0056b3")],
    foreground=[("pressed", "white"), ("active", "white")],
)

# Main popup
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(expand=True, fill="both")

label = ttk.Label(
    main_frame,
    text="OPENEYE has detected your explicit image on Instagram.\nIt has been shared 15 times. Do you want to block it?",
    wraplength=popup_width - 40,  # Wrap text to fit within the popup
    justify="center",
)
label.pack(pady=(20, 20))

button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=(20, 20))

block_button = ttk.Button(button_frame, text="BLOCK", command=on_block)
block_button.pack(side="left", fill="x", expand=True, padx=10)

keep_button = ttk.Button(button_frame, text="KEEP", command=on_keep)
keep_button.pack(side="left", fill="x", expand=True, padx=10)

root.mainloop()
