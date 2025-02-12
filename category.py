from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk, messagebox
import sqlite3

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Akshaj")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # Variables
        self.var_cat_id = StringVar()
        self.var_name = StringVar()
        
        # Title
        lbl_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#184a45", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 30), bg="white")
        lbl_name.place(x=50, y=100)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="lightyellow")
        txt_name.place(x=50, y=170, width=300)

        btn_add = Button(self.root, text="ADD", command=self.add, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_add.place(x=360, y=170, width=150, height=30)

        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="red", fg="white", cursor="hand2")
        btn_delete.place(x=520, y=170, width=150, height=30)

        # Category Details
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=100)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.category_table = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

        self.category_table.heading("cid", text="CID")
        self.category_table.heading("name", text="Name")
        self.category_table["show"] = "headings"
        self.category_table.column("cid", width=90)
        self.category_table.column("name", width=100)
        self.category_table.pack(fill=BOTH, expand=1)
        self.category_table.bind("<ButtonRelease-1>", self.get_data)

        # Images
        self.im1 = Image.open("images/cat.jpg")
        self.im1 = self.im1.resize((500, 250), Image.LANCZOS)
        self.im1 = ImageTk.PhotoImage(self.im1)

        self.lbl_im1 = Label(self.root, image=self.im1)
        self.lbl_im1.place(x=50, y=220)

        self.im2 = Image.open("images/category.jpg")
        self.im2 = self.im2.resize((500, 250), Image.LANCZOS)
        self.im2 = ImageTk.PhotoImage(self.im2)

        self.lbl_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
        self.lbl_im2.place(x=580, y=220)

        self.show()  # Load categories initially

    # Functions
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already present, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO category (name) VALUES (?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category added successfully", parent=self.root)
                    self.show()  # Show updated category list

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.category_table.delete(*self.category_table.get_children())  # Clear current table
            for row in rows:
                self.category_table.insert("", END, values=row)  # Insert new rows
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, event):
        selected_row = self.category_table.focus()  # Get the selected row
        data = self.category_table.item(selected_row)  # Get data of the selected row
        row = data['values']  # Get values
        self.var_cat_id.set(row[0])  # Set category ID
        self.var_name.set(row[1])  # Set category name

    def delete(self):
         con = sqlite3.connect(database=r'ims.db')
         cur = con.cursor()
         try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Select a category to delete", parent=self.root)
            else:
                # Confirm deletion
                confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this category?", parent=self.root)
            if confirm:
                # Use the correct column name for deletion
                cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))  # Assuming 'cid' is the correct column
                con.commit()
                messagebox.showinfo("Success", "Category deleted successfully", parent=self.root)
                self.show()  # Refresh the list
                self.var_cat_id.set("")  # Clear the ID field
                self.var_name.set("")  # Clear the name field

         except Exception as ex:
           messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
         finally:
           con.close()

if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
