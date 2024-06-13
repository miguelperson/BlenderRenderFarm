import pymysql
import tkinter as tk
from tkinter import Label, Scrollbar, Canvas, Frame, Menu, messagebox, Toplevel, Entry, Button

# Root window configuration
root = tk.Tk()
root.state('zoomed')
root.title("Workers Table")

# Define colors and styles for the dark theme
background_color = "#333333"
header_color = "#787878"
text_color = "#FFFFFF"
header_font = ("Helvetica", 12, 'bold')
data_font = ("Arial", 10)
row_colors = ["#333333", "#4a4a4a"]

# Database connection function
def connection():
    return pymysql.connect(host='localhost', user='root', password='7323', db='renderdb')

# Scrollable frame class that fills its container
class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self, bg=background_color, bd=0, highlightthickness=0)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg=background_color)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.bind("<Configure>", self._frame_width)

    def _frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig("all", width=canvas_width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def update_row(row_data):
    update_window = Toplevel(root)
    update_window.title("Update Record")
    update_window.geometry("270x300")
    update_window.configure(bg=background_color)
    update_window.grab_set()  # Focus on this window

    entries = {}
    for index, (desc, value) in enumerate(zip(column_names, row_data)):
        # Frame for each field to improve layout control
        frame = Frame(update_window, bg=background_color)
        frame.grid(row=index, column=0, sticky="ew", padx=10, pady=2)
        frame.grid_columnconfigure(1, weight=1)

        # Labels with improved padding and alignment
        label = Label(frame, text=desc + ":", font=data_font, bg=background_color, fg=text_color)
        label.grid(row=0, column=0, sticky="w")

        # Entry fields with contrast background and visible text cursor
        entry = Entry(frame, fg=text_color, bg="#505050", insertbackground=text_color, relief="flat")
        entry.insert(0, value)
        entry.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        entries[desc] = entry

    def submit_changes():
        updates = ', '.join([f"{key}=%s" for key in entries if key != 'projectID'])
        values = [entry.get() for key, entry in entries.items() if key != 'projectID'] + [row_data[0]]
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE workers SET {updates} WHERE projectID=%s", values)
            conn.commit()
            messagebox.showinfo("Success", "Record updated successfully.", background=background_color, foreground=text_color)
        except Exception as e:
            messagebox.showerror("Error", str(e), background=background_color, foreground=text_color)
        finally:
            cursor.close()
            conn.close()
            update_window.destroy()
            display()

    # Button with visual emphasis and better placement
    submit_button = Button(update_window, text="Submit", command=submit_changes, fg=text_color, bg=header_color)
    submit_button.grid(row=len(column_names), column=0, pady=10, padx=10, sticky="e")

    update_window.grid_rowconfigure(len(column_names), weight=1)  # Give the last row containing the button some weight for better spacing


def delete_row(projectID):
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this row?"):
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM workers WHERE projectID = %s", (projectID,))
            conn.commit()
            messagebox.showinfo("Success", "Row deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()
            display()

def display():
    for widget in root.winfo_children():
        widget.destroy()
    scrollable_frame = ScrollableFrame(root)
    scrollable_frame.pack(fill='both', expand=True)
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workers")
    data = cursor.fetchall()
    global column_names
    column_names = [desc[0] for desc in cursor.description]
    right_click_menu = Menu(root, tearoff=0)
    right_click_menu.add_command(label="Delete")
    right_click_menu.add_command(label="Update")

    def on_right_click(event, row_data):
        right_click_menu.tk_popup(event.x_root, event.y_root)
        right_click_menu.entryconfigure("Delete", command=lambda: delete_row(row_data[0]))
        right_click_menu.entryconfigure("Update", command=lambda: update_row(row_data))

    for index, name in enumerate(column_names):
        header = Label(scrollable_frame.scrollable_frame, text=name, font=header_font, bg=header_color, fg=text_color, relief='ridge')
        header.grid(row=0, column=index, sticky="nsew")
        scrollable_frame.scrollable_frame.grid_columnconfigure(index, weight=1)

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            cell_bg = row_colors[i % 2]
            label = Label(scrollable_frame.scrollable_frame, text=value, font=data_font, fg=text_color, bg=cell_bg, relief='ridge')
            label.grid(row=i + 1, column=j, sticky="nsew")
            label.bind("<Button-3>", lambda event, row_data=row: on_right_click(event, row_data))

    cursor.close()
    conn.close()

display()

root.mainloop()
