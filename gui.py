import tkinter as tk
from tkinter import filedialog

# Browse the file
def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_entry.delete(0, tk.END)  # Clear the textbox
        file_path_entry.insert(0, file_path)  # Insert new file path

# Window
root = tk.Tk()

root.title("Amazing Brain Draining Project")
root.geometry("500x500")

custom_font=('Roboto', 12)

# Grid for path browsing
pathframe = tk.Frame(root)
pathframe.columnconfigure(0, weight=1)
pathframe.columnconfigure(1, weight=1)
pathframe.columnconfigure(2, weight=1)

label = tk.Label(pathframe, text="File Location:", font=custom_font)
label.grid(row=0, column=0, padx=10)

# Create an Entry widget to display the selected file path
file_path_entry = tk.Entry(pathframe, width=40)
file_path_entry.grid(row=0, column=1, padx=10)

# Create a button to trigger the file dialog
browse_button = tk.Button(pathframe, text="Browse", font=custom_font, command=browse_file)
browse_button.grid(row=0, column=2, padx=10)

pathframe.pack(padx=20, pady=20)

root.mainloop()