import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import hashlib
import json
import webbrowser


conn = sqlite3.connect('sonie.db')
c = conn.cursor()


blockchain = []

def submit():
    phone_number = phone_number_entry.get()
    amount = amount_entry.get()

    
    if not (phone_number and amount):
        messagebox.showerror("Error", "Please enter both phone number and amount.")
    elif len(phone_number) != 10 or not phone_number.isdigit():
        messagebox.showerror("Error", "Please enter a valid 10-digit phone number.")
    else:
        pin = simpledialog.askstring("PIN", "Please enter your PIN:", show='*')
        if pin == "0000":
           
            transaction = {
                'phone_number': phone_number,
                'amount': amount,
            }
          
            blockchain.append(transaction)
            
         
            messagebox.showinfo("Transaction Hash", "Transaction Hash: {}".format(hash_transaction(transaction)))
            messagebox.showinfo("Phone Number Hash", "Phone Number Hash: {}".format(hash_data(transaction['phone_number'])))
            messagebox.showinfo("Amount Hash", "Amount Hash: {}".format(hash_data(transaction['amount'])))
            
            
            write_to_html("transactions.html", "Blocks for Previous Transactions", blockchain)
            
          
            submit_button.config(text="Sending...")
            root.update()
            root.after(3000, update_amount, phone_number, amount)
            
           
            render_html_in_browser("transactions.html")
        else:
            messagebox.showerror("Error", "Invalid PIN.")

def hash_data(data):
   
    return hashlib.sha256(data.encode()).hexdigest()

def hash_transaction(transaction):
   
    return hash_data(json.dumps(transaction, sort_keys=True))

def update_amount(phone_number, amount):
   
    c.execute("SELECT * FROM user WHERE phone_number=?", (phone_number,))
    record = c.fetchone()
    if record:
        existing_amount_str = record[4]  
        try:
            existing_amount = int(existing_amount_str) 
            new_amount = existing_amount - int(amount)  
          
            c.execute("UPDATE user SET amount=? WHERE phone_number=?", (new_amount, phone_number))
            conn.commit()
            messagebox.showinfo("Success", "Transaction Successful".format(new_amount))
            submit_button.config(text="Submit")
        except ValueError:
            messagebox.showerror("Error", "Invalid existing amount in the database.")
    else:
        messagebox.showerror("Error", "Phone number '{}' does not exist in the database. Please check the number and try again.".format(phone_number))


def write_to_html(file_name, title, data):
    with open(file_name, 'a') as f: 
        if data:
            previous_block_hash = None
            for i, transaction in enumerate(data):
                f.write("<div class='block'>\n")
                f.write("<h2>Transaction {}</h2>\n".format(i + 1))
                f.write("<div class='transaction'>\n")
                f.write("<p><strong>Transaction Hash:</strong> {}</p>\n".format(hash_transaction(transaction)))
                f.write("<p><strong>Phone Number Hash:</strong> {}</p>\n".format(hash_data(transaction['phone_number'])))
                f.write("<p><strong>Amount Hash:</strong> {}</p>\n".format(hash_data(transaction['amount'])))
                f.write("</div>\n")
                f.write("</div>\n")
                if previous_block_hash is not None:
                    f.write("<div class='block'>\n")
                    f.write("<h2>New Block {}</h2>\n".format(i + 1))
                    f.write("<div class='transaction'>\n")
                    f.write("<p><strong>Previous Block Hash:</strong> {}</p>\n".format(previous_block_hash))
                    new_block_hash = hash_data(previous_block_hash)
                    f.write("<p><strong>New Block Hash:</strong> {}</p>\n".format(new_block_hash))
                    f.write("</div>\n")
                    f.write("</div>\n")
                previous_block_hash = hash_transaction(transaction)
        else:
            f.write("<p>No transactions found.</p>\n")

def render_html_in_browser(file_name):
    webbrowser.open(file_name)
root = tk.Tk()
root.title("Mpesa")


frame = tk.Frame(root, bg='#f0f0f0') 
frame.pack(padx=50, pady=50)
phone_number_label = tk.Label(frame, text="Phone Number:", bg='#f0f0f0')  
phone_number_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
phone_number_entry = tk.Entry(frame)
phone_number_entry.grid(row=0, column=1, padx=10, pady=10)
amount_label = tk.Label(frame, text="Amount:", bg='#f0f0f0')  
amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
amount_entry = tk.Entry(frame)
amount_entry.grid(row=1, column=1, padx=10, pady=10)
submit_button = tk.Button(frame, text="Submit", command=submit, bg='#4caf50', fg='white')  
submit_button.grid(row=2, columnspan=2, padx=10, pady=20)
root.mainloop()
conn.close()
