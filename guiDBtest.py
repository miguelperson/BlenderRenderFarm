#pip install PyMySQL
import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

#connection later

#gui
root = Tk()
root.title("Render Queue")
root.geometry("1080x720")
mt_tree = ttk.Treeview(root)

#functions later

#gui
label=Label(root, text="Render Queue", font=('Arial Bold', 30))
label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

studidLabel=Label(root, text="Stud ID", font=('Arial', 15))
fnameLabel=Label(root, text="First Name", font=('Arial', 15))
lnameLabel=Label(root, text="Last Name", font=('Arial', 15))
addressLabel=Label(root, text="Address", font=('Arial', 15))
phoneLabel=Label(root, text="Phone", font=('Arial', 15))

studidLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
fnameLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
lnameLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
addressLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
phoneLabel.grid(row=7, column=0, columnspan=1, padx=50, pady=5)

#text variable later
studidEntry=Entry(root, width=55,bd=5, font=('Arial', 15))
fnameEntry=Entry(root, width=55,bd=5, font=('Arial', 15))
lnameEntry=Entry(root, width=55,bd=5, font=('Arial', 15))
addressEntry=Entry(root, width=55,bd=5, font=('Arial', 15))
phoneEntry=Entry(root, width=55,bd=5, font=('Arial', 15))

studidEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
fnameEntry.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
lnameEntry.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
addressEntry.grid(row=6, column=1, columnspan=4, padx=5, pady=0)
phoneEntry.grid(row=7, column=1, columnspan=4, padx=5, pady=0)

#command later
addBtn=Button(
    root,text="Add", padx=65, pady=25,width=10, bd=5, font=('Arial', 15),bg="#84F894"
)
updateBth=Button(
    root,text="Update", padx=65, pady=25,width=10, bd=5, font=('Arial', 15),bg="#84E8F8"
)
deleteBth=Button(
    root,text="Delete", padx=65, pady=25,width=10, bd=5, font=('Arial', 15),bg="#FF9999"
)
searchBth=Button(
    root,text="Search", padx=65, pady=25,width=10, bd=5, font=('Arial', 15),bg="#F4FE82"
)
resetBth=Button(
    root,text="Reset", padx=65, pady=25,width=10, bd=5, font=('Arial', 15),bg="#F398FF"
)
selectBth=Button(
    root,text="Select", padx=65, pady=25,width=10, bd=5, font=('Arial', 15),bg="#EEEEEE"
)

addBtn.grid(row=3,column=5,columnspan=1,rowspan=2)
updateBth.grid(row=5,column=5,columnspan=1,rowspan=2)
deleteBth.grid(row=7,column=5,columnspan=1,rowspan=2)
searchBth.grid(row=9,column=5,columnspan=1,rowspan=2)
resetBth.grid(row=11,column=5,columnspan=1,rowspan=2)
selectBth.grid(row=13,column=5,columnspan=1,rowspan=2)



root.mainloop()