import tkinter as tk
from tkinter import filedialog

path_input = ""
path_output= ""

# Browse the path
def browse_path_input():
    global path_input
    file_path = filedialog.askopenfilename()
    if file_path:
        entry1.delete(0, tk.END)  # Clear the textbox
        entry1.insert(0, file_path)  # Insert new file path
        path_input = file_path

def browse_path_output():
    global path_output
    file_path = filedialog.askdirectory()
    if file_path:
        entry2.delete(0, tk.END)  # Clear the textbox
        entry2.insert(0, file_path)  # Insert new file path
        path_output = file_path

# Window
root = tk.Tk()

root.title("Amazing Brain Draining Project")
root.geometry("700x500")
custom_font=('Roboto', 12)


# Grid for path browsing_____________________________________________________________________________(start)
pathframe = tk.Frame(root)
pathframe.columnconfigure(0, weight=1)
pathframe.columnconfigure(1, weight=1)
pathframe.columnconfigure(2, weight=1)

# ROW 1 (INPUT PATH)---------------------------------------------------------------------------------(start)
# Lable (input path)
location_lable = tk.Label(pathframe, text="File Location:", font=custom_font)
location_lable.grid(row=0, column=0, padx=10, sticky="w")

# Entry widget to display the selected directory path (input path)
entry1 = tk.Text(pathframe, height=1, width=40)
entry1.grid(row=0, column=1, padx=10)

# Browse button (input path)
browse_button1 = tk.Button(pathframe, text="Browse", font=custom_font, command= browse_path_input, width=10, height=1)
browse_button1.grid(row=0, column=2, padx=10)
pathframe.pack(padx=10, pady=20)
# ROW 1 (INPUT PATH)-----------------------------------------------------------------------------------(end)

# ROW 2 (OUTPUT PATH)--------------------------------------------------------------------------------(start)
# Lable (output path)
location_lable = tk.Label(pathframe, text="File Destination:", font=custom_font)
location_lable.grid(row=1, column=0, padx=10, sticky="w")

# Entry widget to display the selected directory path (output path)
entry2 = tk.Text(pathframe, height=1, width=40)
entry2.grid(row=1, column=1, padx=10, pady=20)

# Browse button (output path)
browse_button2 = tk.Button(pathframe, text="Browse", font=custom_font, command= browse_path_output, width=10, height=1)
browse_button2.grid(row=1, column=2, padx=10)
pathframe.pack(padx=10, pady=20)
# ROW 2 (OUTPUT PATH)----------------------------------------------------------------------------------(end)
# Grid for path browsing_______________________________________________________________________________(end)

root.mainloop()
print(path_input)
print(path_output)
