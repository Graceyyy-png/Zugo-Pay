import sqlite3
import tkinter as tk
from tkinter import messagebox


def submit_form():
    phone_number = phone_number_entry.get()
    amount = amount_entry.get()

   
    if phone_number == "" or amount == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return

  
    conn = sqlite3.connect('sonie.db')
    c = conn.cursor()

   
    c.execute("SELECT amount FROM user WHERE phone_number=?", (phone_number,))
    existing_customer = c.fetchone()

    if existing_customer is not None:
       
        new_amount = float(existing_customer[0]) + float(amount)
        c.execute("UPDATE user SET amount=? WHERE phone_number=?", (new_amount, phone_number))
        conn.commit()
        messagebox.showinfo("Success", f"Amount updated for Phone Number: {phone_number}. New Amount: {new_amount}")
    else:
       
        c.execute("INSERT INTO user (phone_number, amount) VALUES (?, ?)", (phone_number, amount))
        conn.commit()
        messagebox.showinfo("Success", f"New customer added. Phone Number: {phone_number}, Amount: {amount}")

  
    conn.close()


root = tk.Tk()
root.title("Phone Number and Amount Form")
root.geometry("350x250")

phone_number_label = tk.Label(root, text="Phone Number:")
phone_number_label.grid(row=0, column=0, padx=10, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=1, column=0, padx=10, pady=5)

phone_number_entry = tk.Entry(root)
phone_number_entry.grid(row=0, column=1, padx=10, pady=5)

amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=10, pady=5)


submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=2, columnspan=2, padx=10, pady=10)


root.mainloop()
