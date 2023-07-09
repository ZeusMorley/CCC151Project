import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

# Colors
color1 = '#000000'  # black
color2 = '#0cbd6e'  # green
color3 = '#343434'  # dark gray
color4 = '#b9e3fa'  # light blue
color5 = '#96d8d3'  # dark blue green
color6 = '#e4e4e4'  # light gray
color7 = '#ffa078'  # pastel orange

database = "Project3.db" # Database file

root = tk.Tk()
root.title('Supermarket Product Price Tracker')
root.geometry("600x500")
root.resizable(width=False, height=False)

conn = sqlite3.connect(database)
c = conn.cursor()
'''Tables
c.execute("""CREATE TABLE category(
    category_ID   INTEGER NOT NULL,
    category_name TEXT NOT NULL,
    PRIMARY KEY(category_ID AUTOINCREMENT)
)""")

c.execute("""CREATE TABLE product(
    product_ID    INTEGER NOT NULL,
    product_brand TEXT NOT NULL,
    product_name  TEXT NOT NULL,
    product_variety   TEXT NOT NULL,
    product_size  TEXT NOT NULL,
    category_ID   TEXT,
    FOREIGN KEY(category_ID) REFERENCES category(category_ID) ON DELETE SET NULL,
    PRIMARY KEY(product_ID AUTOINCREMENT)
)""")

c.execute("""CREATE TABLE supermarket(
    supermarket_ID    INTEGER NOT NULL,
    supermarket_name  TEXT NOT NULL,
    street    TEXT NOT NULL,
    barangay  TEXT NOT NULL,
    city  TEXT NOT NULL,
    province  TEXT NOT NULL,
    postal    TEXT NOT NULL,
    PRIMARY KEY(supermarket_ID AUTOINCREMENT)
)""")
'''
# Create a Notebook widget
notebook = ttk.Notebook(root)
notebook.place(relwidth=1, relheight=1)  # Use place() instead of pack()

# Create a custom style for the Notebook tabs
style = ttk.Style()
style.configure('Custom.TNotebook.Tab', font=('Arial', 11, 'bold'))
notebook.configure(style='Custom.TNotebook')

# Create tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)

# Add tabs to the Notebook
notebook.add(tab1, text="PRODUCT")
notebook.add(tab2, text="CATEGORY")
notebook.add(tab3, text="SUPERMARKET")
notebook.add(tab4, text="PRICED")

# Functions --------------------------------------------------------------------------------------------------
def confirm_delete_price():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    param = (chosen_product_ID_delete_price, chosen_supermarket_ID_delete_price)

    query = "SELECT * FROM priced WHERE pproduct_ID = ? AND psupermarket_ID = ?"
    c.execute(query, param)
    records = c.fetchall()
    if records:
        query2 = "DELETE FROM priced WHERE pproduct_ID = ? AND psupermarket_ID = ?"
        c.execute(query2, param)
        messagebox.showinfo("Delete Price", "SUCCESSFULLY DELETED PRICE")
    else:
        messagebox.showinfo("Delete Price", "PRICE FOR THIS PRODUCT IN SUPERMARKET IS EMPTY")
    conn.commit()
    conn.close()

def delete_price():
    global select_prod_label
    global select_sup_label
    global chosen_product_ID_delete_price
    global chosen_supermarket_ID_delete_price

    messagebox.showinfo("INSTRUCTIONS", "When selecting a PRODUCT or SUPERMARKET, DOUBLE CLICK \nyour chosen PRODUCT or SUPERMARKET.")
    
    price_delete = tk.Tk()
    conn = sqlite3.connect(database)
    c = conn.cursor()

    price_delete.title("DELETE PRICE")
    price_delete.geometry("900x200")
    price_delete.resizable(width=False, height=False)
    price_delete.configure(bg=color5)

    select_sup_label = tk.Label(price_delete, text="", font=('Arial', 10, 'bold'), bg=color5)
    select_sup_label.grid(row=0, column=1, pady=(14,0))

    select_prod_label = tk.Label(price_delete, text="", font=('Arial', 10, 'bold'), bg=color5)
    select_prod_label.grid(row=1, column=1, pady=(14,0))

    chosen_product_ID_delete_price = ''
    chosen_supermarket_ID_delete_price = ''

    def confirm_delete_filter():
        if chosen_product_ID_delete_price.strip() == "":
            messagebox.showerror("Input Error", "You need to choose a PRODUCT")
            return

        if chosen_supermarket_ID_delete_price.strip() == "":
            messagebox.showerror("Input Error", "You need to choose a SUPERMARKET")
            return

        confirm_delete_price()
    
    def list_prod3():
        def on_double_click_list_prod3(event):
            global chosen_product_ID_delete_price
            global select_prod_label
            
            if select_prod_label is not None:
                select_prod_label.config(text="")

            select_prod_label.config(text="")
            selected_item = listbox.get(listbox.curselection())
            chosen_product_ID_delete_price = selected_item.split()[0]
            select_prod_label = tk.Label(price_delete, text=selected_item, font=('Arial', 10, 'bold'), bg=color5)
            select_prod_label.update_idletasks()
            select_prod_label.grid(row=1, column=1, pady=(14,0))
            lists.destroy()

        lists = tk.Tk()
        lists.title("LIST OF PRODUCTS")
        lists.geometry("600x300")
        lists.resizable(width=False, height=False)
        lists.configure(bg=color5)

        listbox = tk.Listbox(lists, width=70)
        listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT * FROM product ORDER BY product_ID")
        records = c.fetchall()

        for record in records:
            product_ID = record[0]
            product_brand = record[1]
            product_name = record[2]
            product_variety = record[3]
            product_size = record[4]
            category_ID = record[5]

            cat_name = ''
            query = "SELECT * FROM category WHERE category_ID = ?"
            c.execute(query, (record[5],))
            records2 = c.fetchall()
            for record2 in records2:
                cat_name = record2[1] 

            listbox.insert(tk.END,str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(
                record[3]) + " " + str(record[4]) + " (" + str(cat_name) + ")" + "\n")

            listbox.bind("<Double-Button-1>", on_double_click_list_prod3)
        conn.commit()
        conn.close()

    def list_sup3():
        def on_double_click_list_sup3(event):
            global chosen_supermarket_ID_delete_price
            global select_sup_label

            if select_sup_label is not None:
                select_sup_label.config(text="")

            selected_item = listbox.get(listbox.curselection())
            chosen_supermarket_ID_delete_price = selected_item.split()[0]
            select_sup_label = tk.Label(price_delete, text=selected_item, font=('Arial', 10, 'bold'), bg=color5)
            select_sup_label.update_idletasks()
            select_sup_label.grid(row=0, column=1, pady=(14,0))
            lists.destroy()

        lists = tk.Tk()
        lists.title("LIST OF SUPERMARKETS")
        lists.geometry("600x300")
        lists.resizable(width=False, height=False)
        lists.configure(bg=color5)

        listbox = tk.Listbox(lists, width=70)
        listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT * FROM supermarket ORDER BY supermarket_ID")
        records = c.fetchall()

        for record in records:
            supermarket_ID = record[0]
            supermarket_name = record[1]
            street = record[2]
            barangay = record[3]
            city = record[4]
            province = record[5]
            postal = record[6]

            listbox.insert(tk.END, str(record[0]) + " " + str(record[1]) + " | " + str(record[2]) + " " + str(
                record[3]) + " " + str(record[4]) + " " + str(record[5]) + " " + str(record[6]) + "\n")

        listbox.bind("<Double-Button-1>", on_double_click_list_sup3)
        conn.commit()
        conn.close()

    select_sup_btn = tk.Button(price_delete, text="SELECT SUPERMARKET", font=('Arial', 10, 'bold'), command=list_sup3)
    select_sup_btn.grid(row=0, column=0, padx=20, ipadx=20, pady=10)

    select_prod_btn = tk.Button(price_delete, text="SELECT PRODUCT", font=('Arial', 10, 'bold'), command=list_prod3)
    select_prod_btn.grid(row=1, column=0, ipadx=20, pady=10)

    confirm_set_btn = tk.Button(price_delete, text="DELETE PRICE", font=('Arial', 10, 'bold'), command=confirm_delete_filter)
    confirm_set_btn.grid(row=3, column=0, ipadx=20, pady=10)

def update_sup():
    def on_double_click_update_sup(event):
        global chosen_supermarket_update_ID
        global categoryName_Entry

        def confirm_sup_edit():
            conn = sqlite3.connect(database)
            c = conn.cursor()

            new_supermarket_name = supName_Entry.get()
            new_street = street_Entry.get()
            new_barangay = barangay_Entry.get()
            new_city = city_Entry.get()
            new_province = province_Entry.get()
            new_postal = postalCode_Entry.get()

            query = "UPDATE supermarket SET supermarket_name = ? WHERE supermarket_ID = ? "
            c.execute(query, (new_supermarket_name, chosen_supermarket_update_ID))

            query2 = "UPDATE supermarket SET street = ? WHERE supermarket_ID = ? "
            c.execute(query2, (new_street, chosen_supermarket_update_ID))

            query3 = "UPDATE supermarket SET barangay = ? WHERE supermarket_ID = ? "
            c.execute(query3, (new_barangay, chosen_supermarket_update_ID))

            query4 = "UPDATE supermarket SET city = ? WHERE supermarket_ID = ? "
            c.execute(query4, (new_city, chosen_supermarket_update_ID))

            query5 = "UPDATE supermarket SET province = ? WHERE supermarket_ID = ? "
            c.execute(query5, (new_province, chosen_supermarket_update_ID))

            query6 = "UPDATE supermarket SET postal = ? WHERE supermarket_ID = ? "
            c.execute(query6, (new_postal, chosen_supermarket_update_ID))

            conn.commit()
            conn.close()

            supermarket_btn = tk.Button(tab3, text="ADD SUPERMARKET", font=('Arial', 10, 'bold'), command=sup_filter)
            supermarket_btn.grid(row=7, column=1, ipadx=10)

            messagebox.showinfo("Update Success", "SUCCESSFULLY UPDATED SUPERMARKET")

            supName_Entry.delete(0, tk.END)
            street_Entry.delete(0, tk.END)
            barangay_Entry.delete(0, tk.END)
            city_Entry.delete(0, tk.END)
            province_Entry.delete(0, tk.END)
            postalCode_Entry.delete(0, tk.END)

        selected_item = listbox.get(listbox.curselection())
        chosen_supermarket_update_ID = selected_item.split()[0]

        conn = sqlite3.connect(database)
        c = conn.cursor()   

        query = "SELECT * FROM supermarket WHERE supermarket_ID = ?"
        c.execute(query, (chosen_supermarket_update_ID,))
        records = c.fetchall()

        for record in records:
            if record[1] is not None:
                supName_Entry.insert(0, record[1])
            if record[2] is not None:
                street_Entry.insert(0, record[2])
            if record[3] is not None:
                barangay_Entry.insert(0, record[3])
            if record[4] is not None:
                city_Entry.insert(0, record[4])
            if record[5] is not None:
                province_Entry.insert(0, record[5])
            if record[6] is not None:
                postalCode_Entry.insert(0, record[6])

        supermarket_btn = tk.Button(tab3, text="CONFIRM EDIT", font=('Arial', 10, 'bold'), command=confirm_sup_edit)
        supermarket_btn.grid(row=7, column=1, ipadx=20, padx=(10,0))

        conn.commit()
        conn.close()
        lists.destroy()

    messagebox.showinfo("INSTRUCTIONS", "DOUBLE CLICK THE PRODUCT THAT YOU WANT TO UPDATE.")
    lists = tk.Tk()
    lists.title("LIST OF SUPERMARKETS")
    lists.geometry("500x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM supermarket ORDER BY supermarket_ID")
    records = c.fetchall()

    for record in records:
        supermarket_ID = record[0]
        supermarket_name = record[1]
        street = record[2]
        barangay = record[3]
        city = record[4]
        province = record[5]
        postal = record[6]

        listbox.insert(tk.END, str(record[0]) + " " + str(record[1]) + " | " + str(record[2]) + " " + str(
            record[3]) + " " + str(record[4]) + " " +str(record[5]) + " " +str(record[6]) + "\n")
        listbox.bind("<Double-Button-1>", on_double_click_update_sup)

    conn.commit()
    conn.close()

def delete_sup():
    def on_double_click_delete_sup(event):
        selected_item = listbox.get(listbox.curselection())
        chosen_sup_ID_delete_sup = selected_item.split()[0]

        conn = sqlite3.connect(database)
        c = conn.cursor()

        query = "DELETE FROM supermarket WHERE supermarket_ID = ?"
        c.execute(query, (chosen_sup_ID_delete_sup,))
        
        query2 = "DELETE FROM priced WHERE psupermarket_ID = ?"
        c.execute(query2, (chosen_sup_ID_delete_sup,))

        query3 = "DELETE FROM price_log WHERE lsupermarket_ID = ?"
        c.execute(query2, (chosen_sup_ID_delete_sup,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Delete Success", "SUCCESSFULLY DELETED SUPERMARKET")
        lists.destroy()

    messagebox.showinfo("INSTRUCTIONS", "DOUBLE CLICK THE SUPERMARKET THAT YOU WANT TO DELETE.\nDELETING A SUPERMARKET WILL DELETE ITS PRICINGS IN PRODUCTS")
    lists = tk.Tk()
    lists.title("LIST OF SUPERMARKETS")
    lists.geometry("500x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM supermarket ORDER BY supermarket_ID")
    records = c.fetchall()

    for record in records:
        supermarket_ID = record[0]
        supermarket_name = record[1]
        street = record[2]
        barangay = record[3]
        city = record[4]
        province = record[5]
        postal = record[6]

        listbox.insert(tk.END, str(record[0]) + " "+ str(record[1]) + " | " + str(record[2]) + " " + str(
            record[3]) + " " + str(record[4]) + " " +str(record[5]) + " " +str(record[6]) + "\n")
        listbox.bind("<Double-Button-1>", on_double_click_delete_sup)

    conn.commit()
    conn.close()

def update_prod():
    def on_double_click_update_prod(event):
        global chosen_product_update_ID
        global categoryName_Entry

        def confirm_prod_edit():
            conn = sqlite3.connect(database)
            c = conn.cursor()

            new_brand = brand_Entry.get()
            new_product_name = productName_Entry.get()
            new_variety = variety_Entry.get()
            new_size = size_Entry.get()

            hold_category = category_Entry.get()
            query_a = "SELECT * FROM category WHERE category_name= ?"
            c.execute(query_a, (hold_category,))
            records = c.fetchall()

            if records:
                for record in records:
                    new_category = record[0]

                query_b = "SELECT * FROM category WHERE category_ID= ?"
                c.execute(query_b, (new_category,))

                query = "UPDATE product SET product_brand = ? WHERE product_ID = ? "
                c.execute(query, (new_brand, chosen_product_update_ID))

                query2 = "UPDATE product SET product_name = ? WHERE product_ID = ? "
                c.execute(query2, (new_product_name, chosen_product_update_ID))

                query3 = "UPDATE product SET product_variety = ? WHERE product_ID = ? "
                c.execute(query3, (new_variety, chosen_product_update_ID))

                query4 = "UPDATE product SET product_size = ? WHERE product_ID = ? "
                c.execute(query4, (new_size, chosen_product_update_ID))

                query5 = "UPDATE product SET category_ID = ? WHERE product_ID = ? "
                c.execute(query5, (new_category, chosen_product_update_ID))

            else:
                messagebox.showerror("Update Error", "CATEGORY NAME DOES NOT EXIST")
                return

            conn.commit()
            conn.close()

            product_btn = tk.Button(tab1, text="ADD PRODUCT", font=('Arial', 10, 'bold'), command=prod_filter)
            product_btn.grid(row=6, column=1, ipadx=40, padx=(10,0))

            messagebox.showinfo("Update Success", "SUCCESSFULLY UPDATED PRODUCT")

            brand_Entry.delete(0, tk.END)
            productName_Entry.delete(0, tk.END)
            variety_Entry.delete(0, tk.END)
            size_Entry.delete(0, tk.END)
            category_Entry.delete(0, tk.END)

        selected_item = listbox.get(listbox.curselection())
        chosen_product_update_ID = selected_item.split()[0]

        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT * FROM product WHERE product_ID= " + chosen_product_update_ID)
        records = c.fetchall()

        for record in records:
            if record[1] is not None:
                brand_Entry.insert(0, record[1])
            if record[2] is not None:
                productName_Entry.insert(0, record[2])
            if record[3] is not None:
                variety_Entry.insert(0, record[3])
            if record[4] is not None:
                size_Entry.insert(0, record[4])

            query_c = "SELECT * FROM category WHERE category_ID= ?"
            c.execute(query_c, (record[5],))
            records2 = c.fetchall()

            for record2 in records2:
                global cat_namep
                cat_namep = record2[1]

            category_Entry.insert(0, record2[1])

        product_btn = tk.Button(tab1, text="CONFIRM EDIT", font=('Arial', 10, 'bold'), command=confirm_prod_edit)
        product_btn.grid(row=6, column=1, ipadx=40, padx=(10,0))
    

        conn.commit()
        conn.close()
        lists.destroy()

    messagebox.showinfo("INSTRUCTIONS", "DOUBLE CLICK THE PRODUCT THAT YOU WANT TO UPDATE.")
    lists = tk.Tk()
    lists.title("LIST OF PRODUCTS")
    lists.geometry("500x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM product ORDER BY product_ID")
    records = c.fetchall()

    for record in records:
        product_ID = record[0]
        product_brand = record[1]
        product_name = record[2]
        product_variety = record[3]
        product_size = record[4]
        category_ID = record[5]

        cat_name = ''
        query = "SELECT * FROM category WHERE category_ID = ?"
        c.execute(query, (record[5],))
        records2 = c.fetchall()
        for record2 in records2:
            cat_name = record2[1] 

        listbox.insert(tk.END, str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(
            record[3]) + " " + str(record[4]) + " (" + str(cat_name) + ")" + "\n")
        listbox.bind("<Double-Button-1>", on_double_click_update_prod)

    conn.commit()
    conn.close()

def delete_prod():
    def on_double_click_delete_prod(event):
        selected_item = listbox.get(listbox.curselection())
        chosen_product_ID_delete_prod = selected_item.split()[0]

        conn = sqlite3.connect(database)
        c = conn.cursor()

        query = "DELETE FROM product WHERE product_ID = ?"
        c.execute(query, (chosen_product_ID_delete_prod,))
        
        query2 = "DELETE FROM priced WHERE pproduct_ID = ?"
        c.execute(query2, (chosen_product_ID_delete_prod,))

        query3 = "DELETE FROM price_log WHERE lproduct_ID = ?"
        c.execute(query2, (chosen_product_ID_delete_prod,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Delete Success", "SUCCESSFULLY DELETED PRODUCT")
        lists.destroy()

    messagebox.showinfo("INSTRUCTIONS", "DOUBLE CLICK THE PRODUCT THAT YOU WANT TO DELETE.\nDELETING A PRODUCT WILL DELETE ITS PRICES IN SUPERMARKETS")
    lists = tk.Tk()
    lists.title("LIST OF PRODUCTS")
    lists.geometry("500x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM product ORDER BY product_ID")
    records = c.fetchall()

    for record in records:
        product_ID = record[0]
        product_brand = record[1]
        product_name = record[2]
        product_variety = record[3]
        product_size = record[4]
        category_ID = record[5]

        cat_name = ''
        query = "SELECT * FROM category WHERE category_ID = ?"
        c.execute(query, (record[5],))
        records2 = c.fetchall()
        for record2 in records2:
            cat_name = record2[1] 

        listbox.insert(tk.END, str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(
            record[3]) + " " + str(record[4]) + " (" + str(cat_name) + ")" + "\n")
        listbox.bind("<Double-Button-1>", on_double_click_delete_prod)

    conn.commit()
    conn.close()

def update_cat():
    def on_double_click_update_cat(event):
        global chosen_category_ID
        global categoryName_Entry
        def confirm_cat_edit():
            conn = sqlite3.connect(database)
            c = conn.cursor()
            new_category_name = categoryName_Entry.get()

            query = "SELECT * FROM category where category_name = ?"
            c.execute(query, (new_category_name,))
            records = c.fetchall()
            if records:
                messagebox.showerror("Duplicate Category Name", "THIS CATEGORY NAME ALREADY EXISTS.")
                return
            else:
                query2 = "UPDATE category SET category_name = ? WHERE category_ID = ?"
                c.execute(query2, (new_category_name, chosen_category_ID))
                categoryName_Entry.delete(0, tk.END)

            conn.commit()
            conn.close()

            addCategory_btn = tk.Button(tab2, text="ADD CATEGORY", font=('Arial', 10, 'bold'), command=cat_filter)
            addCategory_btn.grid(row=2, column=1, ipadx=40)
            messagebox.showinfo("Update Success", "SUCCESSFULLY UPDATED CATEGORY")

        selected_item = listbox.get(listbox.curselection())
        chosen_category_ID = selected_item.split()[0]

        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT * FROM category WHERE category_ID= " + chosen_category_ID)
        records = c.fetchall()

        for record in records:
            categoryName_Entry.insert(0, record[1])

        addCategory_btn = tk.Button(tab2, text="CONFIRM EDIT", font=('Arial', 10, 'bold'), command=confirm_cat_edit)
        addCategory_btn.grid(row=2, column=1, ipadx=40, padx=(10,0))

        conn.commit()
        conn.close()
        lists.destroy()

    messagebox.showinfo("INSTRUCTIONS", "DOUBLE CLICK THE CATEGORY THAT YOU WANT TO UPDATE.")
    lists = tk.Tk()
    lists.title("LIST OF CATEGORIES")
    lists.geometry("500x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM category ORDER BY category_ID")
    records = c.fetchall()

    for record in records:
        category_ID = record[0]
        category_name = record[1]

        listbox.insert(tk.END, str(record[0]) + " " + str(record[1]) + "\n")
        listbox.bind("<Double-Button-1>", on_double_click_update_cat)

    conn.commit()
    conn.close()

def delete_cat():
    def on_double_click_delete_cat(event):
        selected_item = listbox.get(listbox.curselection())
        chosen_category_ID = selected_item.split()[0]

        conn = sqlite3.connect(database)
        c = conn.cursor()

        query = "SELECT * FROM product WHERE category_ID = ?"
        c.execute(query, (chosen_category_ID,))
        records = c.fetchall()
        if records:
            messagebox.showerror("Delete Failure", "CANNOT DELETE THIS CATEGORY\nTHIS CATEGORY CONTAINS PRODUCTS\nIF YOU WANT TO DELETE THIS CATEGORY\nPLEASE MOVE THE PRODUCTS TO A DIFFERENT CATEGORY\nOR DELETE THE PRODUCTS BELONGING TO THIS CATEGORY")
            return
        else:
            query2 = "DELETE FROM category WHERE category_ID = ?"
            c.execute(query2, (chosen_category_ID,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Delete Success", "SUCCESSFULLY DELETED CATEGORY")
        lists.destroy()

    messagebox.showinfo("INSTRUCTIONS", "DOUBLE CLICK THE CATEGORY THAT YOU WANT TO DELETE.\nYOU CAN ONLY DELETE AN EMPTY CATEGORY.\n(NO PRODUCTS BELONG TO IT)")
    lists = tk.Tk()
    lists.title("LIST OF CATEGORIES")
    lists.geometry("500x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM category ORDER BY category_ID")
    records = c.fetchall()

    for record in records:
        category_ID = record[0]
        category_name = record[1]

        listbox.insert(tk.END, str(record[0]) + " " + str(record[1]) + "\n")
        listbox.bind("<Double-Button-1>", on_double_click_delete_cat)

    conn.commit()
    conn.close()

def show_history():
    history = tk.Tk()
    history.title("PRICE HISTORY")
    history.geometry("600x300")
    history.resizable(width=False, height=False)
    history.configure(bg=color5)

    listbox = tk.Listbox(history, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(history)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    query = "SELECT * FROM product WHERE product_ID = ?"
    c.execute(query, (chosen_product_ID,))
    records = c.fetchall()
    if records:
        for record in records:
            prod_brand = record[1]
            prod_name = record[2]
            prod_variety = record[3]
            prod_size = record[4]
            prod_cat_ID = record[5]

            cat_name = ''
            query2 = "SELECT * FROM category WHERE category_ID =?"
            c.execute(query2, (record[5],))
            records2 = c.fetchall()
            for record2 in records2:
                cat_name = record2[1]

        query3 = "SELECT * FROM supermarket WHERE supermarket_ID= ?"
        c.execute(query3, (chosen_supermarket_ID,))
        records3 = c.fetchall()

        for record3 in records3:
            sup_name = record3[1]
            sup_barangay = record3[3]
            sup_city = record3[4]

            sup_name = str(sup_name) if sup_name is not None else "None"
            sup_barangay = str(sup_barangay) if sup_barangay is not None else "None"
            sup_city = str(sup_city) if sup_city is not None else "None"

        listbox.insert(tk.END, "Price History of " + str(record[1]) + " " + str(record[2]) + " " + str(record[3])
            + " " + str(record[4]) + " (" + str(record2[1]) + ")")
        listbox.insert(tk.END, "in " + str(record3[1]) + " " + str(record3[3]) + " " + str(record3[4]))

        param = (chosen_product_ID, chosen_supermarket_ID)

        query3 = "SELECT * FROM price_log WHERE lproduct_ID = ? AND lsupermarket_ID = ?"
        c.execute(query3, param)
        records = c.fetchall()

        for record in records:
            lproduct_Price = record[2]
            lprice_date = record[3]

            listbox.insert(tk.END, str(record[2]) + "  (" + str(record[3]) + ") \n")

        listbox.insert(tk.END, "----------END OF PRICE HISTORY----------")
    else:
        listbox.insert(tk.END, "NO PRICE HISTORY AVAILABLE")
    conn.commit()
    conn.close()

def show_history_prompt():
    global select_prod_label
    global select_sup_label
    global chosen_product_ID
    global chosen_supermarket_ID
    global price_set

    messagebox.showinfo("INSTRUCTIONS", "When selecting a PRODUCT or SUPERMARKET, DOUBLE CLICK \nyour chosen PRODUCT or SUPERMARKET.")
    
    price_set = tk.Tk()
    conn = sqlite3.connect(database)
    c = conn.cursor()

    price_set.title("SHOW PRICE HISTORY OF PRODUCT IN SUPERMARKET")
    price_set.geometry("900x200")
    price_set.resizable(width=False, height=False)
    price_set.configure(bg=color5)

    select_sup_label = tk.Label(price_set, text="", font=('Arial', 10, 'bold'), bg=color5)
    select_sup_label.grid(row=0, column=1, pady=(14,0))

    select_prod_label = tk.Label(price_set, text="", font=('Arial', 10, 'bold'), bg=color5)
    select_prod_label.grid(row=1, column=1, pady=(14,0))

    chosen_product_ID = ''
    chosen_supermarket_ID = ''

    def show_history_filter():
        if chosen_product_ID == "":
            messagebox.showerror("Input Error", "You need to choose a PRODUCT")
            return

        if chosen_supermarket_ID == "":
            messagebox.showerror("Input Error", "You need to choose a SUPERMARKET")
            return

        show_history()


    def list_prod2():
        def on_double_click_list_prod2(event):
            global chosen_product_ID
            global select_prod_label
            
            if select_prod_label is not None:
                select_prod_label.config(text="")

            select_prod_label.config(text="")
            selected_item = listbox.get(listbox.curselection())
            chosen_product_ID = selected_item.split()[0]
            select_prod_label = tk.Label(price_set, text=selected_item, font=('Arial', 10, 'bold'), bg=color5)
            select_prod_label.update_idletasks()
            select_prod_label.grid(row=1, column=1, pady=(14,0))
            lists.destroy()

        lists = tk.Tk()
        lists.title("LIST OF PRODUCTS")
        lists.geometry("600x300")
        lists.resizable(width=False, height=False)
        lists.configure(bg=color5)

        listbox = tk.Listbox(lists, width=70)
        listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT * FROM product ORDER BY product_ID")
        records = c.fetchall()

        for record in records:
            product_ID = record[0]
            product_brand = record[1]
            product_name = record[2]
            product_variety = record[3]
            product_size = record[4]
            category_ID = record[5]

            cat_name = ''
            query = "SELECT * FROM category WHERE category_ID = ?"
            c.execute(query, (record[5],))
            records2 = c.fetchall()
            for record2 in records2:
                cat_name = record2[1] 

            listbox.insert(tk.END, str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(
                record[3]) + " " + str(record[4]) + " (" + str(cat_name) + ")" + "\n")

            listbox.bind("<Double-Button-1>", on_double_click_list_prod2)
        conn.commit()
        conn.close()

    def list_sup2():
        def on_double_click_list_sup2(event):
            global chosen_supermarket_ID
            global select_sup_label
            
            if select_sup_label is not None:
                select_sup_label.config(text="")

            selected_item = listbox.get(listbox.curselection())
            chosen_supermarket_ID = selected_item.split()[0]
            select_sup_label = tk.Label(price_set, text=selected_item, font=('Arial', 10, 'bold'), bg=color5)
            select_sup_label.update_idletasks()
            select_sup_label.grid(row=0, column=1, pady=(14,0))
            lists.destroy()

        lists = tk.Tk()
        lists.title("LIST OF SUPERMARKETS")
        lists.geometry("600x300")
        lists.resizable(width=False, height=False)
        lists.configure(bg=color5)

        listbox = tk.Listbox(lists, width=70)
        listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT * FROM supermarket ORDER BY supermarket_ID")
        records = c.fetchall()
        
        for record in records:
            supermarket_ID = record[0]
            supermarket_name = record[1]
            street = record[2]
            barangay = record[3]
            city = record[4]
            province = record[5]
            postal = record[6]

            listbox.insert(tk.END, str(record[0]) + " " + str(record[1]) + " | " + str(record[2]) + " " + str(
                record[3]) + " " + str(record[4]) + " " +str(record[5]) + " " +str(record[6]) + "\n")

        listbox.bind("<Double-Button-1>", on_double_click_list_sup2)
        conn.commit()
        conn.close()

    select_sup_btn = tk.Button(price_set, text="SELECT SUPERMARKET", font=('Arial', 10, 'bold'), command=list_sup2)
    select_sup_btn.grid(row=0, column=0, padx=20, ipadx=20, pady=10)

    select_prod_btn = tk.Button(price_set, text="SELECT PRODUCT", font=('Arial', 10, 'bold'), command=list_prod2)
    select_prod_btn.grid(row=1, column=0, ipadx=20, pady=10)

    confirm_set_btn = tk.Button(price_set, text="SEE HISTORY", font=('Arial', 10, 'bold'), command=show_history_filter)
    confirm_set_btn.grid(row=3, column=0, ipadx=20, pady=10)

    conn.commit()
    conn.close()

def show_prices():
    lists = tk.Tk()
    lists.title("LIST OF PRICES")
    lists.geometry("600x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    listbox.insert(tk.END, "LIST OF PRICES: ")
    c.execute("SELECT * FROM priced ORDER BY pPrice")
    records = c.fetchall()

    for record in records:
        psupermarket_ID = record[0]
        pproduct_ID = record[1]
        pPrice = record[2]
        pDate = record[3]

        sup_name = ''
        query = "SELECT * FROM supermarket WHERE supermarket_ID = ?"
        c.execute(query, (record[0],))
        records2 = c.fetchall()
        for record2 in records2:
            sup_name = record2[1]
            sup_barangay = record2[3]
            sup_city = record2[4]

        prod_name = ''
        query2 = "SELECT * FROM product WHERE product_ID = ?"
        c.execute(query2, (record[1],))
        records3 = c.fetchall()
        for record3 in records3:
            prod_brand = record3[1]
            prod_name = record3[2]
            prod_variety = record3[3]
            prod_size = record3[4]
            prod_cat_ID = record3[5]

            cat_name = ''
            query3 = "SELECT * FROM category WHERE category_ID =?"
            c.execute(query3, (record3[5],))
            records4 = c.fetchall()
            for record4 in records4:
                cat_name = record4[1]

        listbox.insert(tk.END,"------")
        listbox.insert(tk.END, str(record2[1]) + " " + str(record2[3]) + " " + str(record2[4]))
        listbox.insert(tk.END, str(record3[1]) + " " + str(record3[2]) + " " + str(record3[3]) + " " + str(record3[4]) + " (" + str(cat_name) + ")")
        listbox.insert(tk.END, "P" + str(record[2]) + " (" + str(record[3]) + ")")
        listbox.insert(tk.END, "------")
        listbox.insert(tk.END, "")

    conn.commit()
    conn.close()

def confirm_set():
    def set_price():
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("INSERT INTO priced VALUES(:psupermarket_ID, :pproduct_ID, :pPrice, :pDate)",
            {
                'psupermarket_ID': chosen_supermarket_ID,
                'pproduct_ID': chosen_product_ID,
                'pPrice': Price_Entry.get(),
                'pDate': Date_Entry.get()
            })

        c.execute("INSERT INTO price_log VALUES(:lsupermarket_ID, :lproduct_ID, :lPrice, :lDate)",
            {
                'lsupermarket_ID': chosen_supermarket_ID,
                'lproduct_ID': chosen_product_ID,
                'lPrice': Price_Entry.get(),
                'lDate': Date_Entry.get()
            })

        Price_Entry.delete(0, tk.END)
        Date_Entry.delete(0, tk.END)

        messagebox.showinfo("Set Price", "SETTING PRICE AND DATE SUCCESSFUL.")
        price_set.destroy()
        conn.commit()
        conn.close()

    price_set = tk.Tk()
    conn = sqlite3.connect(database)
    c = conn.cursor()

    price_set.title("Set price")
    price_set.geometry("200x100")
    price_set.resizable(width=False, height=False)
    price_set.configure(bg=color5)

    Price_Label = tk.Label(price_set, text="PRICE", font=('Arial', 12, 'bold'), fg=color1, bg=color5)
    Price_Label.grid(row=0, column=0)

    Date_Label = tk.Label(price_set, text="DATE", font=('Arial', 12, 'bold'), fg=color1, bg=color5)
    Date_Label.grid(row=1, column=0)

    Price_Entry = tk.Entry(price_set, width=20, fg=color1, bg=color6)
    Price_Entry.grid(row=0, column=1)

    Date_Entry = tk.Entry(price_set, width=20, fg=color1, bg=color6)
    Date_Entry.grid(row=1, column=1)

    set_price_btn = tk.Button(price_set, text="CONFIRM", font=('Arial', 10, 'bold'), fg=color3, bg=color7, command=set_price)
    set_price_btn.grid(row=5, column=1)

    query = "SELECT * FROM priced WHERE pproduct_ID = ? AND psupermarket_ID = ?"
    param = (chosen_product_ID, chosen_supermarket_ID)

    c.execute(query, param)

    records = c.fetchall()

    if records:
        for record in records:
            Price_Entry.insert(0, record[2])
            Date_Entry.insert(0, record[3]) 

        query2 = "DELETE FROM priced WHERE pproduct_ID = ? AND psupermarket_ID = ?"
        c.execute(query2, param)

    conn.commit()
    conn.close()

def set_price():
    global select_prod_label
    global select_sup_label
    global price_set
    global chosen_product_ID
    global chosen_supermarket_ID

    messagebox.showinfo("INSTRUCTIONS", "When selecting a PRODUCT or SUPERMARKET, DOUBLE CLICK \nyour chosen PRODUCT or SUPERMARKET.")
    
    price_set = tk.Tk()
    conn = sqlite3.connect(database)
    c = conn.cursor()

    price_set.title("SET PRICE")
    price_set.geometry("900x200")
    price_set.resizable(width=False, height=False)
    price_set.configure(bg=color5)

    select_sup_label = tk.Label(price_set, text="", font=('Arial', 10, 'bold'), bg=color5)
    select_sup_label.grid(row=0, column=1, pady=(14,0))

    select_prod_label = tk.Label(price_set, text="", font=('Arial', 10, 'bold'), bg=color5)
    select_prod_label.grid(row=1, column=1, pady=(14,0))

    chosen_product_ID = ''
    chosen_supermarket_ID = ''

    def confirm_set_filter():
        if chosen_product_ID.strip() == "":
            messagebox.showerror("Input Error", "You need to choose a PRODUCT")
            return

        if chosen_supermarket_ID.strip() == "":
            messagebox.showerror("Input Error", "You need to choose a SUPERMARKET")
            return

        confirm_set()
    
    def list_prod2():
        def on_double_click_list_prod2(event):
            global chosen_product_ID
            global select_prod_label
            
            if select_prod_label is not None:
                select_prod_label.config(text="")

            select_prod_label.config(text="")
            selected_item = listbox.get(listbox.curselection())
            chosen_product_ID = selected_item.split()[0]
            select_prod_label = tk.Label(price_set, text=selected_item, font=('Arial', 10, 'bold'), bg=color5)
            select_prod_label.update_idletasks()
            select_prod_label.grid(row=1, column=1, pady=(14,0))
            lists.destroy()

        lists = tk.Tk()
        lists.title("LIST OF PRODUCTS")
        lists.geometry("600x300")
        lists.resizable(width=False, height=False)
        lists.configure(bg=color5)

        listbox = tk.Listbox(lists, width=70)
        listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT * FROM product ORDER BY product_ID")
        records = c.fetchall()

        for record in records:
            product_ID = record[0]
            product_brand = record[1]
            product_name = record[2]
            product_variety = record[3]
            product_size = record[4]
            category_ID = record[5]

            cat_name = ''
            query = "SELECT * FROM category WHERE category_ID = ?"
            c.execute(query, (record[5],))
            records2 = c.fetchall()
            for record2 in records2:
                cat_name = record2[1] 

            listbox.insert(tk.END,str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(
                record[3]) + " " + str(record[4]) + " (" + str(cat_name) + ")" + "\n")

            listbox.bind("<Double-Button-1>", on_double_click_list_prod2)
        conn.commit()
        conn.close()

    def list_sup2():
        def on_double_click_list_sup2(event):
            global chosen_supermarket_ID
            global select_sup_label

            if select_sup_label is not None:
                select_sup_label.config(text="")

            selected_item = listbox.get(listbox.curselection())
            chosen_supermarket_ID = selected_item.split()[0]
            select_sup_label = tk.Label(price_set, text=selected_item, font=('Arial', 10, 'bold'), bg=color5)
            select_sup_label.update_idletasks()
            select_sup_label.grid(row=0, column=1, pady=(14,0))
            lists.destroy()

        lists = tk.Tk()
        lists.title("LIST OF SUPERMARKETS")
        lists.geometry("600x300")
        lists.resizable(width=False, height=False)
        lists.configure(bg=color5)

        listbox = tk.Listbox(lists, width=70)
        listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(lists)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("SELECT * FROM supermarket ORDER BY supermarket_ID")
        records = c.fetchall()

        for record in records:
            supermarket_ID = record[0]
            supermarket_name = record[1]
            street = record[2]
            barangay = record[3]
            city = record[4]
            province = record[5]
            postal = record[6]

            listbox.insert(tk.END, str(record[0]) + " " + str(record[1]) + " | " + str(record[2]) + " " + str(
                record[3]) + " " + str(record[4]) + " " +str(record[5]) + " " +str(record[6]) + "\n")

        listbox.bind("<Double-Button-1>", on_double_click_list_sup2)
        conn.commit()
        conn.close()

    select_sup_btn = tk.Button(price_set, text="SELECT SUPERMARKET", font=('Arial', 10, 'bold'), command=list_sup2)
    select_sup_btn.grid(row=0, column=0, padx=20, ipadx=20, pady=10)

    select_prod_btn = tk.Button(price_set, text="SELECT PRODUCT", font=('Arial', 10, 'bold'), command=list_prod2)
    select_prod_btn.grid(row=1, column=0, ipadx=20, pady=10)

    confirm_set_btn = tk.Button(price_set, text="SET PRICE", font=('Arial', 10, 'bold'), command=confirm_set_filter)
    confirm_set_btn.grid(row=3, column=0, ipadx=20, pady=10)

    conn.commit()
    conn.close()

def sup_filter():
    # Get the values from the entry widgets and convert to lowercase
    supermarket_name = supName_Entry.get().lower()
    street = street_Entry.get().lower()
    barangay = barangay_Entry.get().lower()
    city = city_Entry.get().lower()
    province = province_Entry.get().lower()
    postal = postalCode_Entry.get().lower()

    # Check if any required entry is empty
    if not supermarket_name:
        messagebox.showerror("Input Error", "You cannot input a blank!")
        return

    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Execute a SELECT statement with named parameters to filter the supermarkets
    c.execute(
        "SELECT * FROM supermarket WHERE LOWER(supermarket_name) = :supermarket_name "
        "AND LOWER(street) = :street AND LOWER(barangay) = :barangay "
        "AND LOWER(city) = :city AND LOWER(province) = :province AND LOWER(postal) = :postal",
        {
            'supermarket_name': supermarket_name,
            'street': street,
            'barangay': barangay,
            'city': city,
            'province': province,
            'postal': postal
        }
    )

    # Fetch the result
    result = c.fetchone()

    conn.close()

    # Check if a matching supermarket was found
    if result is not None:
        messagebox.showinfo("Supermarket Exists", "THIS SUPERMARKET ALREADY EXISTS.")
        # Clear the entry widgets
        supName_Entry.delete(0, tk.END)
        street_Entry.delete(0, tk.END)
        barangay_Entry.delete(0, tk.END)
        city_Entry.delete(0, tk.END)
        province_Entry.delete(0, tk.END)
        postalCode_Entry.delete(0, tk.END)
    else:
        add_sup()

def cat_filter():
    category_name = categoryName_Entry.get().lower()

    if not category_name:
        messagebox.showerror("Input Error", "You cannot input a blank!")
        return

    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Execute the query to check if the category already exists
    query = "SELECT * FROM category WHERE LOWER(category_name) = LOWER(?)"
    c.execute(query, (category_name,))
    records = c.fetchall()

    if not records:
        add_cat()
    else:
        messagebox.showerror("Category Error", "Category already exists in the database.")

def prod_filter():
    # Get the values from the entry widgets and convert to lowercase
    product_brand = brand_Entry.get().lower()
    product_name = productName_Entry.get().lower()
    product_variety = variety_Entry.get().lower()
    product_size = size_Entry.get().lower()
    category_name = category_Entry.get().lower()

    # Check if any required entry is empty
    if not product_brand or not product_name or not category_name:
        messagebox.showerror("Input Error", "You cannot input a blank!")
        return

    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Check if the category name exists
    query4 = "SELECT * FROM category WHERE LOWER(category_name) = LOWER(?)"
    c.execute(query4, (category_name,))
    records = c.fetchall()

    if not records:
        messagebox.showerror("Category Error", "CATEGORY DOES NOT EXIST.\nPlease enter a valid category name.")
        return

    # Execute a SELECT statement with named parameters to check if the product exists
    c.execute(
        "SELECT * FROM product WHERE LOWER(product_brand) = :product_brand AND LOWER(product_name) = :product_name "
        "AND LOWER(product_variety) = :product_variety AND LOWER(product_size) = :product_size AND LOWER(category_ID) = :category_ID",
        {
            'product_brand': product_brand,
            'product_name': product_name,
            'product_variety': product_variety,
            'product_size': product_size,
            'category_ID': category_name
        }
    )

    # Fetch the result
    result = c.fetchone()
    conn.commit()
    conn.close()

    # Check if a matching product was found
    if result is not None:
        messagebox.showinfo("Product Exists", "THIS PRODUCT ALREADY EXISTS.")
        # Clear the entry widgets
        brand_Entry.delete(0, tk.END)
        productName_Entry.delete(0, tk.END)
        variety_Entry.delete(0, tk.END)
        size_Entry.delete(0, tk.END)
        category_Entry.delete(0, tk.END)

    else:
        add_prod()

def search_sup():
    search = supSearch_Entry.get()
    if search.strip() == "":
        messagebox.showerror("Input Error", "You cannot Input a blank!")
        return

    counter = 0
    search_list = tk.Tk()
    search_list.title('SUPERMARKET SEARCH RESULTS')
    search_list.geometry("600x400")
    search_list.resizable(width=False, height=False)
    search_list.configure(bg=color5)

    listbox = tk.Listbox(search_list, width=80)
    listbox.config(font=('Arial', 12, 'bold'))
    listbox.config(bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(search_list)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    listbox.insert(tk.END, "You searched for: " + search)
    listbox.insert(tk.END, "")

    c.execute("SELECT * FROM supermarket WHERE supermarket_name LIKE ?", ('%' + search + '%',))
    records = c.fetchall()

    if records:
        counter += 1
        listbox.insert(tk.END, "------ Supermarket Name match -----")

        for record in records:
            supermarket_ID = record[0]
            supermarket_name = record[1]
            street = record[2]
            barangay = record[3]
            city = record[4]
            province = record[5]
            postal = record[6]

            listbox.insert(tk.END,
                        str(record[0]) + " " + "(" + str(record[1]) + ") " + str(record[2]) + " " + str(record[3]) + 
                           " " + str(record[4]) + " " + str(record[5]) + " " + str(record[6]) + "\n")
        listbox.insert(tk.END, "------END of Supermarket Name match -----")
        listbox.insert(tk.END, "")

    c.execute("SELECT * FROM supermarket WHERE street LIKE ?", ('%' + search + '%',))
    records2 = c.fetchall()

    if records2:
        counter += 1
        listbox.insert(tk.END, "------ Street match -----")

        for record2 in records2:
            supermarket_ID = record2[0]
            supermarket_name = record2[1]
            street = record2[2]
            barangay = record2[3]
            city = record2[4]
            province = record2[5]
            postal = record2[6]

            listbox.insert(tk.END,
                           str(record[0]) + " " + str(record2[1]) + " (" + str(record2[2]) + ") " + str(record2[3]) + 
                           " " + str(record2[4]) + " " + str(record2[5]) + " " + str(record2[6]) + "\n")
        listbox.insert(tk.END, "------END of Street match -----")
        listbox.insert(tk.END, "")

    c.execute("SELECT * FROM supermarket WHERE barangay LIKE ?", ('%' + search + '%',))
    records3 = c.fetchall()

    if records3:
        counter += 1
        listbox.insert(tk.END, "------ Barangay match -----")

        for record3 in records3:
            supermarket_ID = record3[0]
            supermarket_name = record3[1]
            street = record3[2]
            barangay = record3[3]
            city = record3[4]
            province = record3[5]
            postal = record3[6]

            listbox.insert(tk.END,
                           str(record[0]) + " " + str(record3[1]) + " " + str(record3[2]) + " (" + str(record3[3]) + 
                           ") " + str(record3[4]) + " " + str(record3[5]) + " " + str(record3[6]) + "\n")
        listbox.insert(tk.END, "------END of Barangay match -----")
        listbox.insert(tk.END, "")

    c.execute("SELECT * FROM supermarket WHERE city LIKE ?", ('%' + search + '%',))
    records4 = c.fetchall()

    if records4:
        counter += 1
        listbox.insert(tk.END, "------ City match -----")

        for record4 in records4:
            supermarket_ID = record4[0]
            supermarket_name = record4[1]
            street = record4[2]
            barangay = record4[3]
            city = record4[4]
            province = record4[5]
            postal = record4[6]

            listbox.insert(tk.END,
                           str(record[0]) + " " + str(record4[1]) + " " + str(record4[2]) + "  " + str(record4[3]) + 
                           " (" + str(record4[4]) + ") " + str(record4[5]) + " " + str(record4[6]) + "\n")
        listbox.insert(tk.END, "------END of City match -----")
        listbox.insert(tk.END, "")

    c.execute("SELECT * FROM supermarket WHERE province LIKE ?", ('%' + search + '%',))
    records5 = c.fetchall()

    if records5:
        counter += 1
        listbox.insert(tk.END, "------ Province match -----")

        for record5 in records5:
            supermarket_ID = record5[0]
            supermarket_name = record5[1]
            street = record5[2]
            barangay = record5[3]
            city = record5[4]
            province = record5[5]
            postal = record5[6]

            listbox.insert(tk.END,
                           str(record[0]) + " " + str(record5[1]) + " " + str(record5[2]) + " " + str(record5[3]) + 
                           " " + str(record5[4]) + " (" + str(record5[5]) + ") " + str(record5[6]) + "\n")
        listbox.insert(tk.END, "------END of Province match -----")
        listbox.insert(tk.END, "")

    c.execute("SELECT * FROM supermarket WHERE postal LIKE ?", ('%' + search + '%',))
    records6 = c.fetchall()

    if records6:
        counter += 1
        listbox.insert(tk.END, "------ Postal match -----")

        for record6 in records6:
            supermarket_ID = record6[0]
            supermarket_name = record6[1]
            street = record6[2]
            barangay = record6[3]
            city = record6[4]
            province = record6[5]
            postal = record6[6]

            listbox.insert(tk.END,
                           str(record[0]) + " " + str(record6[1]) + " " + str(record6[2]) + " " + str(record6[3]) + 
                           " " + str(record6[4]) + " " + str(record6[5]) + " (" + str(record6[6]) + ")\n")
        listbox.insert(tk.END, "------END of Postal match -----")
        listbox.insert(tk.END, "")

    if counter == 0:
        listbox.insert(tk.END, "No Results found for " + search + ".")

    search_Entry.delete(0, tk.END)

    conn.commit()
    conn.close()

def search_cat():
    search = catSearch_Entry.get()
    if search.strip() == "":
        messagebox.showerror("Input Error", "You cannot Input a blank!")
        return

    counter = 0
    search_list = tk.Tk()
    search_list.title('PRODUCT SEARCH RESULTS')
    search_list.geometry("600x400")
    search_list.resizable(width=False, height=False)
    search_list.configure(bg=color5)

    listbox = tk.Listbox(search_list, width=80)
    listbox.config(font=('Arial', 12, 'bold'))
    listbox.config(bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(search_list)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    listbox.insert(tk.END, "You searched for: " + search)
    listbox.insert(tk.END, "")

    c.execute("SELECT * FROM category WHERE category_name LIKE ?", ('%' + search + '%',))
    records = c.fetchall()

    if records:
        counter += 1
        listbox.insert(tk.END, "------ Category name match -----")

        for record in records:
            category_ID = record[0]
            category_name = record[1]

            listbox.insert(tk.END,
                           str(record[0]) + " (" + str(record[1]) + ") " + "\n")
        listbox.insert(tk.END, "------END of Category Name match -----")
        listbox.insert(tk.END, "")

    if counter == 0:
        listbox.insert(tk.END, "No Results found for " + search + ".")

    search_Entry.delete(0, tk.END)

    conn.commit()
    conn.close()

def search_prod():
    search = search_Entry.get()
    if search.strip() == "":
        messagebox.showerror("Input Error", "You cannot Input a blank!")
        return

    counter = 0
    search_list = tk.Tk()
    search_list.title('PRODUCT SEARCH RESULTS')
    search_list.geometry("600x400")
    search_list.resizable(width=False, height=False)
    search_list.configure(bg=color5)

    listbox = tk.Listbox(search_list, width=80)
    listbox.config(font=('Arial', 12, 'bold'))
    listbox.config(bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(search_list)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    listbox.insert(tk.END, "You searched for: " + search)
    listbox.insert(tk.END, "")

    c.execute("SELECT * FROM product WHERE product_brand LIKE ?", ('%' + search + '%',))
    records1 = c.fetchall()

    if records1:
        counter += 1
        listbox.insert(tk.END, "------ Product brand match -----")

        for record1 in records1:
            product_ID = record1[0]
            product_brand = record1[1]
            product_name = record1[2]
            product_variety = record1[3]
            product_size = record1[4]
            category_ID = record1[5]

            cat_name = ''
            query = "SELECT * FROM category WHERE category_ID = ?"
            c.execute(query, (record1[5],))
            recordsc = c.fetchall()
            for recordc in recordsc:
                cat_name = recordc[1] 

            listbox.insert(tk.END,
                           str(record1[0]) + " (" + str(record1[1]) + ") " + str(record1[2]) + "  " + str(record1[3]) + 
                           " " + str(record1[4]) + " [" + cat_name + "]\n")
        listbox.insert(tk.END, "------END of Product brand match -----")
        listbox.insert(tk.END, "")

    c.execute("SELECT * FROM product WHERE product_name LIKE ?", ('%' + search + '%',))
    records2 = c.fetchall()

    if records2:
        counter += 1
        listbox.insert(tk.END, "------ Product Name match -----")

        for record2 in records2:
            product_ID = record2[0]
            product_brand = record2[1]
            product_name = record2[2]
            product_variety = record2[3]
            product_size = record2[4]
            category_ID = record2[5]

            cat_name = ''
            query = "SELECT * FROM category WHERE category_ID = ?"
            c.execute(query, (record2[5],))
            recordsc = c.fetchall()
            for recordc in recordsc:
                cat_name = recordc[1] 

            listbox.insert(tk.END,
                           str(record2[0]) + " " + str(record2[1]) + " (" + str(record2[2]) + ") " + str(record2[3]) + 
                           " " + str(record2[4]) + " [" + cat_name + "]\n")
        listbox.insert(tk.END, "------END of Product Name match -----")
        listbox.insert(tk.END, "")

    c.execute("SELECT * FROM product WHERE product_variety LIKE ?", ('%' + search + '%',))
    records3 = c.fetchall()

    if records3:
        counter += 1
        listbox.insert(tk.END, "------ Product Variety match -----")

        for record3 in records3:
            product_ID = record3[0]
            product_brand = record3[1]
            product_name = record3[2]
            product_variety = record3[3]
            product_size = record3[4]
            category_ID = record3[5]

            cat_name = ''
            query = "SELECT * FROM category WHERE category_ID = ?"
            c.execute(query, (record3[5],))
            recordsc = c.fetchall()
            for recordc in recordsc:
                cat_name = recordc[1] 

            listbox.insert(tk.END,
                           str(record3[0]) + " " + str(record3[1]) + " " + str(record3[2]) + " (" + str(record3[3]) + 
                           ") " + str(record3[4]) + " [" + cat_name + "]\n")
        listbox.insert(tk.END, "------END of Product Variety match -----")
        listbox.insert(tk.END, "")

    c.execute("SELECT * FROM product WHERE product_size LIKE ?", ('%' + search + '%',))
    records4 = c.fetchall()

    if records4:
        counter += 1
        listbox.insert(tk.END, "------ Product Size match -----")

        for record4 in records4:
            product_ID = record4[0]
            product_brand = record4[1]
            product_name = record4[2]
            product_variety = record4[3]
            product_size = record4[4]
            category_ID = record4[5]

            cat_name = ''
            query = "SELECT * FROM category WHERE category_ID = ?"
            c.execute(query, (record4[5],))
            records = c.fetchall()
            for recordc in recordsc:
                cat_name = recordc[1] 

            listbox.insert(tk.END,
                           str(record4[0]) + " " + str(record4[1]) + " " + str(record4[2]) + " " + str(record4[3]) + 
                           " (" + str(record4[4]) + ") [" + cat_name + "]\n")
        listbox.insert(tk.END, "------END of Product Size match -----")
        listbox.insert(tk.END, "")

    if counter == 0:
        listbox.insert(tk.END, "No Results found for " + search + ".")

    search_Entry.delete(0, tk.END)

    conn.commit()
    conn.close()

def list_sup():
    lists = tk.Tk()
    lists.title("LIST OF SUPERMARKETS")
    lists.geometry("600x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM supermarket ORDER BY supermarket_name")
    records = c.fetchall()

    for record in records:
        supermarket_name = record[1]
        street = record[2]
        barangay = record[3]
        city = record[4]
        province = record[5]
        postal = record[6]

        listbox.insert(tk.END, str(record[1]) + " | " + str(record[2]) + " " + str(
            record[3]) + " " + str(record[4]) + " " +str(record[5]) + " " +str(record[6]) + "\n")

    conn.commit()
    conn.close()

def list_cat():
    lists = tk.Tk()
    lists.title("LIST OF Categories")
    lists.geometry("300x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM category ORDER BY category_name")
    records = c.fetchall()

    for record in records:
        category_name = record[1]
        listbox.insert(tk.END, str(record[1]) + "\n")

    conn.commit()
    conn.close()

def list_prod():
    lists = tk.Tk()
    lists.title("LIST OF PRODUCTS")
    lists.geometry("600x300")
    lists.resizable(width=False, height=False)
    lists.configure(bg=color5)

    listbox = tk.Listbox(lists, width=70)
    listbox.config(font=('Arial', 12, 'bold'), bg=color5, fg=color3)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(lists)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM product ORDER BY product_brand")
    records = c.fetchall()

    for record in records:
        product_brand = record[1]
        product_name = record[2]
        product_variety = record[3]
        product_size = record[4]
        category_ID = record[5]

        cat_name = ''
        query = "SELECT * FROM category WHERE category_ID = ?"
        c.execute(query, (record[5],))
        records2 = c.fetchall()
        for record2 in records2:
            cat_name = record2[1] 

        listbox.insert(tk.END, str(record[1]) + " " + str(record[2]) + " " + str(
            record[3]) + " " + str(record[4]) + " (" + str(cat_name) + ")" + "\n")

    conn.commit()
    conn.close()

def add_prod():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Get the values from the entry widgets
    product_brand = brand_Entry.get()
    product_name = productName_Entry.get()
    product_variety = variety_Entry.get()
    product_size = size_Entry.get()

    name_cat = category_Entry.get()
    query = "SELECT * FROM category WHERE category_name = ?"
    c.execute(query, (name_cat,))
    records = c.fetchall()

    for record in records:
        category_ID = record[0]

    # Execute the INSERT statement with named parameters
    c.execute(
        "INSERT INTO product (product_brand, product_name, product_variety, product_size, category_ID) VALUES "
        "(:product_brand, :product_name, :product_variety, :product_size, :category_ID)",
        {
            'product_brand': product_brand,
            'product_name': product_name,
            'product_variety': product_variety,
            'product_size': product_size,
            'category_ID': category_ID
        }
    )

    conn.commit()
    conn.close()

    # Clear the entry widgets
    brand_Entry.delete(0, tk.END)
    productName_Entry.delete(0, tk.END)
    variety_Entry.delete(0, tk.END)
    size_Entry.delete(0, tk.END)
    category_Entry.delete(0, tk.END)

def add_cat():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Get the category name from the entry widget
    category_name = categoryName_Entry.get()

    # Execute the INSERT statement with named parameters
    c.execute("INSERT INTO category (category_name) VALUES (:category_name)", {'category_name': category_name})

    conn.commit()
    conn.close()

    # Clear the entry widget
    categoryName_Entry.delete(0, tk.END)

def add_sup():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Get the values from the entry widgets
    supermarket_name = supName_Entry.get()
    street = street_Entry.get()
    barangay = barangay_Entry.get()
    city = city_Entry.get()
    province = province_Entry.get()
    postal = postalCode_Entry.get()

    # Execute the INSERT statement without the supermarket ID
    c.execute(
        "INSERT INTO supermarket (supermarket_name, street, barangay, city, province, postal) VALUES (:supermarket_name, :street, :barangay, :city, :province, :postal)",
        {
            'supermarket_name': supermarket_name,
            'street': street,
            'barangay': barangay,
            'city': city,
            'province': province,
            'postal': postal
        })

    conn.commit()
    conn.close()

    # Clear the entry widgets
    supName_Entry.delete(0, tk.END)
    street_Entry.delete(0, tk.END)
    barangay_Entry.delete(0, tk.END)
    city_Entry.delete(0, tk.END)
    province_Entry.delete(0, tk.END)
    postalCode_Entry.delete(0, tk.END)

# End of Functions ----------------------------------------------------------------------------


# Labels and Entry Boxes for Tab 1 (PRODUCT)
product_label = tk.Label(tab1, text="PRODUCTS", font=('Arial', 12, 'bold'))
product_label.grid(row=0, column=0, padx=10, pady=10)

brand_label = tk.Label(tab1, text="Brand", font=('Arial', 11))
brand_label.grid(row=1, column=0, padx=10, pady=10)

productName_label = tk.Label(tab1, text="Name", font=('Arial', 11))
productName_label.grid(row=2, column=0, padx=10, pady=10)

variety_label = tk.Label(tab1, text="Variety", font=('Arial', 11))
variety_label.grid(row=3, column=0, padx=10, pady=10)

size_label = tk.Label(tab1, text="Size", font=('Arial', 11))
size_label.grid(row=4, column=0, padx=10, pady=10)

categoryProduct_label = tk.Label(tab1, text="Category", font=('Arial', 11))
categoryProduct_label.grid(row=5, column=0, padx=10, pady=10)

search_label = tk.Label(tab1, text="SEARCH", font=('Arial', 11))
search_label.grid(row=1, column=2)

#PRODUCT ENTRY--------------------------------------------------
brand_Entry = tk.Entry(tab1, width=30)
brand_Entry.grid(row=1, column=1, padx=10, pady=10)

productName_Entry = tk.Entry(tab1, width=30)
productName_Entry.grid(row=2, column=1, padx=10, pady=10)

variety_Entry = tk.Entry(tab1, width=30)
variety_Entry.grid(row=3, column=1, padx=10, pady=10)

size_Entry = tk.Entry(tab1, width=30)
size_Entry.grid(row=4, column=1, padx=10, pady=10)

category_Entry = tk.Entry(tab1, width=30)
category_Entry.grid(row=5, column=1, padx=10, pady=10)

search_Entry = tk.Entry(tab1, width=30)
search_Entry.grid(row=1, column=3, padx=10, pady=10)

# PRODUCT BUTTONS----------------------------------------------------------------------------------
product_btn = tk.Button(tab1, text="ADD PRODUCT", font=('Arial', 10, 'bold'), command=prod_filter)
product_btn.grid(row=6, column=1, ipadx=40)

productSearch_btn = tk.Button(tab1, text="SEARCH PRODUCT", font=('Arial', 10, 'bold'), command=search_prod)
productSearch_btn.grid(row=2, column=3, ipadx=25)

productList_btn = tk.Button(tab1, text="GET LIST", font=('Arial', 10, 'bold'), command=list_prod)
productList_btn.grid(row=3, column=3, ipadx=55)

productUpdate_btn = tk.Button(tab1, text="UPDATE", font=('Arial', 10, 'bold'), command=update_prod)
productUpdate_btn.grid(row=4, column=3, ipadx=60)

productDelete_btn = tk.Button(tab1, text="DELETE", font=('Arial', 10, 'bold'), command=delete_prod)
productDelete_btn.grid(row=5, column=3, ipadx=60)

#CATEGORY-------------------------------------------------------------------------------------------
# Labels and Entry Boxes for Tab 1 (PRODUCT)
category_label = tk.Label(tab2, text="CATEGORY", font=('Arial', 12, 'bold'))
category_label.grid(row=0, column=0, padx=10, pady=10)

categoryName_label = tk.Label(tab2, text="NAME", font=('Arial', 11))
categoryName_label.grid(row=1, column=0, padx=10, pady=10)

catSearch_label = tk.Label(tab2, text="SEARCH", font=('Arial', 11))
catSearch_label.grid(row=3, column=0)

#CATEGORY ENTRY--------------------------------------------------
categoryName_Entry = tk.Entry(tab2, width=30)
categoryName_Entry.grid(row=1, column=1, padx=10, pady=10)

catSearch_Entry = tk.Entry(tab2, width=30)
catSearch_Entry.grid(row=3, column=1, padx=10, pady=10)

#CATEGORY BUTTONS----------------------------------------------------------------------------------
addCategory_btn = tk.Button(tab2, text="ADD CATEGORY", font=('Arial', 10, 'bold'), command=cat_filter)
addCategory_btn.grid(row=2, column=1, ipadx=40)

catSearch_btn = tk.Button(tab2, text="SEARCH CATEGORY", font=('Arial', 10, 'bold'), command=search_cat)
catSearch_btn.grid(row=4, column=1, ipadx=25)

catList_btn = tk.Button(tab2, text="GET LIST", font=('Arial', 10, 'bold'), command=list_cat)
catList_btn.grid(row=1, column=3, padx=30, ipadx=55, pady=10)

catUpdate_btn = tk.Button(tab2, text="UPDATE", font=('Arial', 10, 'bold'), command=update_cat)
catUpdate_btn.grid(row=2, column=3, padx=30, ipadx=60, pady=10)

catDelete_btn = tk.Button(tab2, text="DELETE", font=('Arial', 10, 'bold'), command=delete_cat)
catDelete_btn.grid(row=3, column=3, padx=30, ipadx=60, pady=10)

#SUPERMARKET---------------------------------------------------------------------------------------
supermarket_label = tk.Label(tab3, text="SUPERMARKET", font=('Arial', 12, 'bold'))
supermarket_label.grid(row=0, column=0, padx=10, pady=10)

supName_label = tk.Label(tab3, text="Name", font=('Arial', 11))
supName_label.grid(row=1, column=0, padx=10, pady=10)

street_label = tk.Label(tab3, text="Street", font=('Arial', 11))
street_label.grid(row=2, column=0, padx=10, pady=10)

barangay_label = tk.Label(tab3, text="Barangay", font=('Arial', 11))
barangay_label.grid(row=3, column=0, padx=10, pady=10)

city_label = tk.Label(tab3, text="City", font=('Arial', 11))
city_label.grid(row=4, column=0, padx=10, pady=10)

province_label = tk.Label(tab3, text="Province", font=('Arial', 11))
province_label.grid(row=5, column=0, padx=10, pady=10)

postalCode_label = tk.Label(tab3, text="Postal Code", font=('Arial', 11))
postalCode_label.grid(row=6, column=0, padx=10, pady=10)

supSearch_label = tk.Label(tab3, text="SEARCH", font=('Arial', 11))
supSearch_label.grid(row=1, column=2, padx=10, pady=10)

#SUPERMARKET ENTRY--------------------------------------------------
supName_Entry = tk.Entry(tab3, width=25)
supName_Entry.grid(row=1, column=1, padx=5, pady=10)

street_Entry = tk.Entry(tab3, width=25)
street_Entry.grid(row=2, column=1, padx=5, pady=10)

barangay_Entry = tk.Entry(tab3, width=25)
barangay_Entry.grid(row=3, column=1, padx=5, pady=10)

city_Entry = tk.Entry(tab3, width=25)
city_Entry.grid(row=4, column=1, padx=5, pady=10)

province_Entry = tk.Entry(tab3, width=25)
province_Entry.grid(row=5, column=1, padx=5, pady=10)

postalCode_Entry = tk.Entry(tab3, width=25)
postalCode_Entry.grid(row=6, column=1, padx=5, pady=10)

supSearch_Entry = tk.Entry(tab3, width=25)
supSearch_Entry.grid(row=1, column=3, padx=5, pady=10)

# SUPERMARKET BUTTONS----------------------------------------------------------------------------------
supermarket_btn = tk.Button(tab3, text="ADD SUPERMARKET", font=('Arial', 10, 'bold'), command=sup_filter)
supermarket_btn.grid(row=7, column=1, ipadx=10)

supSearch_btn = tk.Button(tab3, text="SEARCH ", font=('Arial', 10, 'bold'), command=search_sup)
supSearch_btn.grid(row=2, column=3, ipadx=45)

supList_btn = tk.Button(tab3, text="GET LIST", font=('Arial', 10, 'bold'), command=list_sup)
supList_btn.grid(row=3, column=3, ipadx=45)

supUpdate_btn = tk.Button(tab3, text="UPDATE", font=('Arial', 10, 'bold'), command=update_sup)
supUpdate_btn.grid(row=4, column=3, ipadx=50)

supDelete_btn = tk.Button(tab3, text="DELETE", font=('Arial', 10, 'bold'), command=delete_sup)
supDelete_btn.grid(row=5, column=3, ipadx=50)

#PRICED-------------------------------------------------------------------------------------------
price_label = tk.Label(tab4, text="Price", font=('Arial', 12, 'bold'))
price_label.grid(row=0, column=0)

priceAdd_btn = tk.Button(tab4, text="SET ", height=2,  font=('Arial', 10, 'bold'), command=set_price)
priceAdd_btn.grid(row=1, column=0, padx=35, pady=20, ipadx=50)

priceDelete_btn = tk.Button(tab4, text="DELETE", height=2, font=('Arial', 10, 'bold'), command=delete_price)
priceDelete_btn.grid(row=2, column=0, padx=10, pady=20, ipadx=40)

priceList_btn = tk.Button(tab4, text="LIST ", height=2, font=('Arial', 10, 'bold'), command=show_prices)
priceList_btn.grid(row=1, column=1, ipadx=50)

priceHistory_btn = tk.Button(tab4, text="HISTORY", height=2, font=('Arial', 10, 'bold'), command=show_history_prompt)
priceHistory_btn.grid(row=1, column=2, ipadx=45, padx=35)

conn.commit()
conn.close()
root.mainloop()