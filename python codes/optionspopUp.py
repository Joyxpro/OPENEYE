import tkinter as tk
from tkinter import ttk, messagebox


def on_ok():
    selected_option = option_var.get()
    messagebox.showinfo(
        "Selection", f"Now OPENEYE will be monitoring the web {selected_option.lower()}"
    )
    root.destroy()


root = tk.Tk()
root.title("OPENEYE")

# Disable the close button (X)
root.protocol("WM_DELETE_WINDOW", lambda: None)

# Increase the size of the popup box
popup_width = 500
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
style.configure("TLabel", font=("Helvetica", 12), padding=10)
style.configure(
    "TButton",
    font=("Helvetica", 12),
    padding=5,
    background="SystemButtonFace",
    foreground="black",
    borderwidth=0,
)
style.map(
    "TButton",
    background=[("active", "SystemButtonFace")],
    foreground=[("pressed", "black"), ("active", "black")],
)

style.configure("TCombobox", font=("Helvetica", 12), padding=5)

# Main popup
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(expand=True, fill="both")

label = ttk.Label(
    main_frame,
    text="Message from OPENEYE :\nDo you want to monitor the web for your explicit contents?",
)
label.pack(pady=(0, 20))

option_var = tk.StringVar(value="Continuously")

options = ["Continuously", "Hourly", "Daily"]
dropdown = ttk.Combobox(
    main_frame, textvariable=option_var, values=options, state="readonly"
)
dropdown.pack(pady=(0, 10))

ok_button = ttk.Button(main_frame, text="OK", command=on_ok)
ok_button.pack(pady=(20, 0))

root.mainloop()
