import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import ctypes as ct
import customtkinter
import os
from Client import send_file_to_server, recieverFunction, connectionFunction, disconnectMessage# importing client backend so we can call functions from the backend in this code
#---------------------------------------------------------------------------------------------------------------------------------------------

path_output = ""
render_output = ""
start_frame = 0
end_frame = 0
client = None
username = ""
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

HOST = '192.168.99.124'  # Server's IP, change this if the server is reset at any point
PORT = 65432

root = customtkinter.CTk()  # custmtkinter becomes the main type thing to regard the main frame
root.geometry("800x300")
root.title('ESA Blender Render Farm')

#---------------------------------------------------------------------------------------------------------------------------------------------

def handle_error():
    messagebox.showerror('Error', 'Unable to connect to server, please close program and re-open')
    label = customtkinter.CTkLabel(master=frame, text='No Connection', font=("Times New Roman", 22), text_color="red")  # header
    label.grid(row=4, column=0, pady=7, padx=5)

def filePath():
    file_path = filedialog.askopenfilename(
        filetypes=[("Blender Files", "*.blend")],
        initialdir="/",  # Set the initial directory as needed
        title="Select a Blender File"
    )
    if file_path:  # file path is true
        path_output = file_path
        entry1.insert(0, path_output)


def printThing():
    file_path = filedialog.askdirectory()
    if file_path:  # file path is true
        render_output = file_path
        entry2.insert(0, render_output)


def frameChecker(stringOfSomething):
    framesToRender = frameEntry.get().replace(" ", "")
    print(framesToRender)
    framesToRender = framesToRender.split('-')
    if len(framesToRender) == 2 and framesToRender[0].isnumeric() == True and framesToRender[1].isnumeric() == True:
        global start_frame
        global end_frame
        start_frame = int(framesToRender[0])
        end_frame = int(framesToRender[1])
        print(start_frame)
        print(end_frame)
        return True  # input for the frames range is valid
    else:
        return False


def inputErrorMessage(errorType):
    print(f'{errorType} is the error you made')
    if errorType == 1:  # indicates that blend file and/or output folder paths are invalid
        messagebox.showerror('Error', 'Please ensure that blend file/output file path inputs are valid')
    elif errorType == 2:  # indicates invalid frames string
        messagebox.showerror('Error', 'butt inspection will begin immediately')

def submission():
    global client
    if (entry1.get() and entry2.get() and frameEntry.get()) == "":  # this statement checks that all the textfields are filled out, if one is missing execute if statement
        print('please make sure you fill all the file requirements')  # prints if a textfield is missing an input
        inputErrorMessage(1)  # error 1 would indicate that the file paths are not correctly set
    elif frameChecker(frameEntry.get()) == False:  # after first if check that the frame number entry thing is a valid input
        print('please ensure the proper format for your frame entry')
        inputErrorMessage(2)
    elif start_frame > end_frame:
        print('invalid parameters for frame range')
        inputErrorMessage(3)
    else:  # this would be the block we execute if we pass all the previous conditions
        #getting the username
        file_path = entry1.get() ## ============================ going to want to add exception handling becuase if a user presses the submission button with nothing in the entry fields
        # an exception happens as theres nothing instantiated there, would probably be best to include the file_path getter inside the try catch block
        #getting the username from the path
        path_components = file_path.split("/")
        try:
            users_index = path_components.index("Users")
        except ValueError:
            print("Error: 'Users' directory not found in the file path.")
            exit()
        if users_index + 1 < len(path_components):
            username = path_components[users_index + 1]
        else:
            print("Error: Unable to extract username from the file path.")

        send_file_to_server(entry1.get(), entry2.get(), start_frame, end_frame, client, username) # passes through the blender file location, output folder, start frame, and end frame
        recieverFunction(client, outputFolder) # this code will be responsible for recieving the files from the server

    print(entry1.get())
    print(entry2.get())
    print(frameEntry.get())
    print(start_frame)
    print(end_frame)
    print(username)

#User Settings Window
#---------------------------------------------------------------------------------------------------------------------------------------------
def userSettings():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    newWindow = tk.Toplevel(root)
    newWindow.title("User Settings")
    newWindow.configure(bg="black")

    # Set appearance mode and default color theme for the new window
    customtkinter.set_appearance_mode("dark")  # Set to dark mode
    customtkinter.set_default_color_theme("dark-blue")  # Set the color theme to dark blue

    usernameLabel = customtkinter.CTkLabel(newWindow, text="Username: ")
    usernameLabel.grid(row=0, column=0, pady=7, padx=5)

    ipLabel = customtkinter.CTkLabel(newWindow, text="IP address: ")
    ipLabel.grid(row=1, column=0, pady=7, padx=5)

    userEntry = customtkinter.CTkEntry(newWindow, placeholder_text="ex. Sherlock Holmes", width=200)
    userEntry.grid(row=0, column=1, pady=7, padx=5)

    ipEntry = customtkinter.CTkEntry(newWindow, placeholder_text="ex. 192.158.1.38", width=200)
    ipEntry.grid(row=1, column=1, pady=7, padx=5)

    addButton = customtkinter.CTkButton(newWindow, text="Add User")
    addButton.grid(row=3, column=0, pady=7, padx=5)

    replaceButton = customtkinter.CTkButton(newWindow, text="Update User Info")
    replaceButton.grid(row=3, column=1, pady=7, padx=5)


def disconnectHandling():
    disconnectMessage(client) # calls disconnectMessage function from client backend to send '!DISCONNECT' to server

#---------------------------------------------------------------------------------------------------------------------------------------------

#Main window GUI fragments
#---------------------------------------------------------------------------------------------------------------------------------------------
frame = customtkinter.CTkFrame(master=root)

frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="ESA Distributed Rendering", font=("Times New Roman", 22))  
label.grid(row=0, column=0, pady=7, padx=5)

blenderFilePath = customtkinter.CTkLabel(master=frame, text="Blend File Path", font=("Times New Roman", 20))
blenderFilePath.grid(row=1, column=0, pady=7, padx=5)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Blend file path", width=200)
entry1.grid(row=1, column=1, pady=7, padx=5)

button = customtkinter.CTkButton(master=frame, text="Blender File Path", command=filePath)
button.grid(row=1, column=2, pady=7, padx=5)

outputFolder = customtkinter.CTkLabel(master=frame, text="Output Folder", font=("Times New Roman", 20))
outputFolder.grid(row=2, column=0, pady=7, padx=5)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Output File Path", width=200)
entry2.grid(row=2, column=1, pady=7)

outputFilePath = customtkinter.CTkButton(master=frame, text="Output Path", command=printThing)
outputFilePath.grid(row=2, column=2, pady=7)

framesLabel = customtkinter.CTkLabel(master=frame, text='Frames needing rendered (inclusive)', font=("Times New Roman", 20))
framesLabel.grid(row=3, column=0, pady=7, padx=7)

frameEntry = customtkinter.CTkEntry(master=frame, placeholder_text='###-### <- input format', width=200)
frameEntry.grid(row=3, column=1, pady=7, padx=7)

submitButton = customtkinter.CTkButton(master=frame, text='Submit', command=submission)
submitButton.grid(row=4, column=1, pady=7, padx=5)

editUserButton = customtkinter.CTkButton(master=frame, text='User Settings', command=userSettings)
editUserButton.grid(row=5, column=0, pady=7, padx=5)

disconnectButton = customtkinter.CTkButton(master=frame, text='Disconnect', command=disconnectHandling)
disconnectButton.grid(row=5, column=2, pady=7, padx=5)
#---------------------------------------------------------------------------------------------------------------------------------------------

client = connectionFunction(HOST, PORT, error_callback=handle_error) # attempts to connect to the server, execute 'handle_error' function if connection fails

file = customtkinter.CTk

root.mainloop()
