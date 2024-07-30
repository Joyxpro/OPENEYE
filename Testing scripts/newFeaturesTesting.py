import tkinter as tk
from tkinter import ttk, messagebox


def on_select(event):
    selected_option = option_var.get()
    messagebox.showinfo(
        "Selection", f"Now our app will monitor the web {selected_option.lower()}"
    )
    root.destroy()


root = tk.Tk()
root.title("Web Monitor")

# Increase the size of the popup box
popup_width = 400
popup_height = 200

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the popup
center_x = int(screen_width / 2 - popup_width / 2)
center_y = int(screen_height / 2 - popup_height / 2)

# Set the geometry of the window
root.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")

# Main popup
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

label = tk.Label(
    main_frame, text="Do you want to monitor the web for your explicit contents?"
)
label.pack(pady=(0, 10))

option_var = tk.StringVar(value="Continuously")

options = ["Continuously", "Hourly", "Daily"]
dropdown = ttk.Combobox(
    main_frame, textvariable=option_var, values=options, state="readonly"
)
dropdown.pack(pady=(0, 10))

dropdown.bind("<<ComboboxSelected>>", on_select)

root.mainloop()
