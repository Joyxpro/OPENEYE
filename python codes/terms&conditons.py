import tkinter as tk
import webbrowser


def open_terms_and_conditions():
    # Replace with the path or URL to your terms and conditions HTML page
    terms_url = "C:\\Users\\JOY SENGUPTA\\Desktop\\code playground\\OPENEYE\\test.html"
    webbrowser.open(terms_url)


def on_agree():
    # Handle the agree action here
    print("User agreed to the terms and conditions.")
    root.destroy()


def on_disagree():
    # Handle the disagree action here
    print("User disagreed with the terms and conditions.")
    root.destroy()


# Create the main application window
root = tk.Tk()
root.title("Terms and Conditions")
root.geometry("400x200")  # Set window size (width x height)

# Create and place the label with the message
message_label = tk.Label(
    root, text="Do you agree with our terms and conditions of our app?", wraplength=350
)
message_label.pack(pady=20)

# Create and place the link icon
link_icon = tk.Label(root, text="🔗", font=("Arial", 14), cursor="hand2")
link_icon.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)
link_icon.bind("<Button-1>", lambda e: open_terms_and_conditions())

# Create and place the Agree and Disagree buttons
agree_button = tk.Button(root, text="AGREE", command=on_agree)
agree_button.pack(side=tk.LEFT, padx=20, pady=10)

disagree_button = tk.Button(root, text="DISAGREE", command=on_disagree)
disagree_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Start the Tkinter event loop
root.mainloop()
