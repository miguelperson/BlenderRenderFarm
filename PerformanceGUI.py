import pymysql
import tkinter as tk
from tkinter import Label, Scrollbar, Canvas, Frame, Menu, messagebox

# Root window configuration
root = tk.Tk()
root.state('zoomed')
root.title("Performance Table")

# Define colors and styles for the dark theme
background_color = "#333333"
header_color = "#666666"
text_color = "#FFFFFF"
header_font = ("Helvetica", 12, 'bold')
data_font = ("Arial", 10)
row_colors = ["#333333", "#404040"]

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

        # Enable mouse scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Update the canvas scrolling region on configuration change
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.bind("<Configure>", self._frame_width)

    def _frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig("all", width=canvas_width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Function to delete a row from the database
def delete_row(projectID):
    # Confirm before deletion
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this row?"):
        conn = connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM performance WHERE projectID = %s", (projectID,))
            conn.commit()
            messagebox.showinfo("Success", "Row deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()
        display()  # Refresh the display after deletion

# Display data including headers with dynamic column widths
def display():
    for widget in root.winfo_children():
        widget.destroy()

    scrollable_frame = ScrollableFrame(root)
    scrollable_frame.pack(fill='both', expand=True)

    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM performance")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    right_click_menu = Menu(root, tearoff=0)
    selected_row = None  # Variable to store the selected row data

    def on_right_click(event, row_data):
        nonlocal selected_row
        selected_row = row_data
        right_click_menu.tk_popup(event.x_root, event.y_root)
        right_click_menu.entryconfigure("Delete", command=lambda: delete_row(selected_row[0]))

    right_click_menu.add_command(label="Delete")  # Add Delete menu without command

    # Add headers and configure columns for equal distribution
    for index, name in enumerate(column_names):
        header = Label(scrollable_frame.scrollable_frame, text=name, font=header_font, bg=header_color, fg=text_color, relief='ridge')
        header.grid(row=0, column=index, sticky="nsew")
        scrollable_frame.scrollable_frame.grid_columnconfigure(index, weight=1)

    # Display data in labels with automatic stretching and bind right-click event
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
