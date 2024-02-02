import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import ctypes as ct
import customtkinter
from ClientBackEnd import connectionFunction  # importing client backend so we can call functions from the backend in this code

# color pallete
# ededed
# 666666
# ffffff
# 2e2e2e
path_output = ""
render_output = ""
start_frame = 0
end_frame = 0

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()  # custmtkinter becomes the main type thing to regard the main frame
root.geometry("800x400")
root.title('ESA Blender Render Farm')


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
    if (
            entry1.get() and entry2.get() and frameEntry.get()) == "":  # this statement checks that all the textfields are filled out, if one is missing execute if statement
        print('please make sure you fill all the file requirements')  # prints if a textfield is missing an input
        inputErrorMessage(1)  # error 1 would indicate that the file paths are not correctly set
    elif frameChecker(
            frameEntry.get()) == False:  # after first if check that the frame number entry thing is a valid input
        print('please ensure the proper format for your frame entry')
        inputErrorMessage(2)
    elif start_frame > end_frame:
        print('this isnt done right man')
        inputErrorMessage(3)
    else:  # this would be the block we execute if we pass all the previous conditions
        print('place holder where we will execute the data transmission segment')


#    print(entry1.get())
#    print(entry2.get())
#    print(frameEntry.get())
#    print(start_frame)
#    print(end_frame)

frame = customtkinter.CTkFrame(master=root)

frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text='ESA Distributed Rendering', font=("Times New Roman", 22))  # header
label.grid(row=0, column=0, pady=7, padx=5)

blenderFilePath = customtkinter.CTkLabel(master=frame, text='Blend File Path', font=("Times New Roman", 20))
blenderFilePath.grid(row=1, column=0, pady=7, padx=5)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Blend file path", width=200)
entry1.grid(row=1, column=1, pady=7, padx=5)

button = customtkinter.CTkButton(master=frame, text="Blender File Path", command=filePath)
button.grid(row=1, column=2, pady=7, padx=5)

outputFolder = customtkinter.CTkLabel(master=frame, text='Output Folder', font=("Times New Roman", 20))
outputFolder.grid(row=2, column=0, pady=7, padx=5)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Output File Path", width=200)
entry2.grid(row=2, column=1, pady=7)

outputFilePath = customtkinter.CTkButton(master=frame, text="Output Path", command=printThing)
outputFilePath.grid(row=2, column=2, pady=7)

# checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
# checkbox.grid(row=3,column=2,pady=7,padx=7)

framesLabel = customtkinter.CTkLabel(master=frame, text='Frames needing rendered (inclusive)',
                                     font=("Times New Roman", 20))
framesLabel.grid(row=3, column=0, pady=7, padx=7)

frameEntry = customtkinter.CTkEntry(master=frame, placeholder_text='###-### <- input format', width=200)
frameEntry.grid(row=3, column=1, pady=7, padx=7)

submitButton = customtkinter.CTkButton(master=frame, text='Submit', command=submission)
submitButton.grid(row=4, column=1, pady=7, padx=5)

connectionFunction(error_callback=handle_error)  # attempts to connect to the server

file = customtkinter.CTk

root.mainloop()
