import tkinter as tk
import subprocess

def open_client_gui():
    subprocess.Popen(["python", "ClientCustomGUI.py"])

def open_performance_gui():
    subprocess.Popen(["python", "PerformanceGUI.py"])

def open_project_gui():
    subprocess.Popen(["python", "ProjectGUI.py"])

def open_workers_gui():
    subprocess.Popen(["python", "WorkersGUI.py"])

def open_render_gui():
    subprocess.Popen(["python", "RenderGUI.py"])


root = tk.Tk()
root.title("Main Menu")
root.geometry("300x250")

# Menu Button for Performance GUI
client_button = tk.Button(root, text="Client GUI", command=open_client_gui)
client_button.pack(pady=10)

performance_button = tk.Button(root, text="Performance Table", command=open_performance_gui)
performance_button.pack(pady=10)

project_button = tk.Button(root, text="Project GUI", command=open_project_gui)
project_button.pack(pady=10)

workers_button = tk.Button(root, text="Workers GUI", command=open_workers_gui)
workers_button.pack(pady=10)

render_button = tk.Button(root, text="Render GUI", command=open_render_gui)
render_button.pack(pady=10)



root.mainloop()
