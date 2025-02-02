import hashlib
import time
import json
import webbrowser

class Block:
    def __init__(self, index, previous_hash, timestamp, data, current_hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.current_hash = current_hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", calculate_hash(0, "0", time.time(), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    current_hash = calculate_hash(index, previous_block.current_hash, timestamp, data)
    return Block(index, previous_block.current_hash, timestamp, data, current_hash)

def send_mpesa_payment(phone_number, amount):
    print(f"Sending {amount} KES to {phone_number} via M-Pesa")

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

html_content = "<html>\n<body>\n"
html_content += "<h1>Sending Blocks</h1>\n"  # Add heading

for i in range(1, 4):
    data = f"Transaction {i}"

    phone_number = "+2547XXXXXXXX" 
    amount = 100 
    send_mpesa_payment(phone_number, amount)

    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)
    previous_block = new_block

    # Add block information to the HTML content
    html_content += "<pre>" + json.dumps(vars(new_block), indent=2) + "</pre>\n"
    html_content += "<hr>\n"

html_content += "</body>\n</html>"

# Write HTML content to the transaction.html file
with open("transaction.html", "w") as html_file:
    html_file.write(html_content)

# Open the generated HTML file in the default web browser
webbrowser.open("transaction.html")
