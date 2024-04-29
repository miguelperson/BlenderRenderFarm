#pip install PyMySQL
import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

#connection
def connection():
   conn=pymysql.connect(host='localhost',user='root',password='7323', db='renderdb') 
   return conn

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='',index='end',iid=array,text="",values=(array),tag="orow")

    my_tree.tag_configure('orow',background='#EEEEEE',font=('Arial',12))
    my_tree.grid(row=8,column=0,columnspan=5,rowspan=11,padx=10,pady=20)




#gui
root = Tk()
root.title("Render Performance")
root.geometry("1500x720")
my_tree = ttk.Treeview(root)

#functions later
def read():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM performance")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def add():
    studid=str(studidEntry.get())
    fname=str(fnameEntry.get)
    lname=str(addressEntry.get())
    address=str(addressEntry.get())
    phone=str(phoneEntry.get())

#gui
label=Label(root, text="Render Performance", font=('Arial Bold', 30))
label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

studidLabel=Label(root, text="Project ID", font=('Arial', 15))
fnameLabel=Label(root, text="Worker Name", font=('Arial', 15))
lnameLabel=Label(root, text="Frames Total", font=('Arial', 15))
addressLabel=Label(root, text="Time Total", font=('Arial', 15))
phoneLabel=Label(root, text="Start Time", font=('Arial', 15))


studidLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
fnameLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
lnameLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
addressLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
phoneLabel.grid(row=7, column=0, columnspan=1, padx=50, pady=5)

#text variable
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

#command
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

style=ttk.Style()
style.configure("Treeview.Heading",font=('Arial Bold',15))
my_tree['columns'] = ("projectID", "workerID", "frames_total", "time_total", "start_time", "end_time", "worker1_avg_time", "worker2_avg_time")


my_tree.column("#0", width=0,stretch=YES)
my_tree.column("projectID", anchor=W,width=150)
my_tree.column("workerID", anchor=W,width=150)
my_tree.column("frames_total", anchor=W,width=150)
my_tree.column("time_total", anchor=W,width=165)
my_tree.column("start_time", anchor=W,width=150)
my_tree.column("end_time", anchor=W,width=150)
my_tree.column("worker1_avg_time", anchor=W,width=150)
my_tree.column("worker2_avg_time", anchor=W,width=150)

my_tree.heading("projectID",text="Project ID",anchor=W)
my_tree.heading("workerID",text="Worker Name",anchor=W)
my_tree.heading("frames_total",text="Frames Total",anchor=W)
my_tree.heading("time_total",text="Time Total",anchor=W)
my_tree.heading("start_time",text="Start Time",anchor=W)
my_tree.heading("end_time",text="End Time",anchor=W)
my_tree.heading("worker1_avg_time",text="W1 Time",anchor=W)
my_tree.heading("worker2_avg_time",text="W2 Time",anchor=W)

refreshTable()

root.mainloop()