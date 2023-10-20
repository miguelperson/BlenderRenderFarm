import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import info
#import main
import socket

# Browse the path
def browse_path_input():
    global path_input
    file_path = filedialog.askopenfilename()
    if file_path:
        entry1.delete(1.0, tk.END)  # Clear the textbox
        entry1.insert(1.0, file_path)  # Insert new file path
        path_input = file_path

def browse_path_output():
    global path_output
    file_path = filedialog.askdirectory()
    if file_path:
        entry2.delete(1.0, tk.END)  # Clear the textbox
        entry2.insert(1.0, file_path)  # Insert new file path
        path_output = file_path

# Send the info to another file
def send_info():
    global path_input, path_output
    result = info.process_input(path_input, path_output, r.get())
    # Display the result in a message box
    messagebox.showinfo("Result", result)
    
# Window
root = tk.Tk()
root.title("Amazing Brain Draining Project")
root.geometry("700x300")
custom_font=('Roboto', 12)

#variables
path_input = ""
path_output= ""
r = tk.IntVar()
r.set(0)

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
entry1 = tk.Text(pathframe, height=1, width=30)
entry1.grid(row=0, column=1, padx=10)

# Browse button (input path)
browse_button1 = tk.Button(pathframe, text="Browse", font=custom_font, command= browse_path_input, width=10, height=1)
browse_button1.grid(row=0, column=2, padx=10)
pathframe.pack(padx=10, pady=10)
# ROW 1 (INPUT PATH)-----------------------------------------------------------------------------------(end)

# ROW 2 (OUTPUT PATH)--------------------------------------------------------------------------------(start)
# Lable (output path)
location_lable = tk.Label(pathframe, text="Output Destination:", font=custom_font)
location_lable.grid(row=1, column=0, padx=10, sticky="w")

# Entry widget to display the selected directory path (output path)
entry2 = tk.Text(pathframe, height=1, width=30)
entry2.grid(row=1, column=1, padx=10, pady=10)

# Browse button (output path)
browse_button2 = tk.Button(pathframe, text="Browse", font=custom_font, command= browse_path_output, width=10, height=1)
browse_button2.grid(row=1, column=2, padx=10)
# ROW 2 (OUTPUT PATH)----------------------------------------------------------------------------------(end)
pathframe.pack(padx=10, pady=(50, 10))
# Grid for path browsing_______________________________________________________________________________(end)

# Grid radio buttons (video/image)___________________________________________________________________(start)
radioframe = tk.Frame(root)
radioframe.columnconfigure(0, weight=1)
radioframe.columnconfigure(1, weight=1)

r_video = tk.Radiobutton(radioframe, text='Video', font=custom_font, variable=r, value=1)
r_video.grid(row=0, column=0, padx=10)
r_image = tk.Radiobutton(radioframe, text='Image', font=custom_font, variable=r, value=2)
r_image.grid(row=0, column=1, padx=10)

radioframe.pack(padx=10, pady=10)
# Grid radio buttons(video/image)______________________________________________________________________(end)

# Submit button (sends input info)
submit_button = tk.Button(root, text="Submit", font=custom_font, command= send_info, width=10, height=2) # button event handler executes the 'send_info' function when clicked
submit_button.pack(padx=10, pady=10)


root.mainloop()