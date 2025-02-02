import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import hashlib
import time
sns.set(style="whitegrid")

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
blockchain = [create_genesis_block()]
previous_block = blockchain[0]
for i in range(1, 6):
    data = f"Transaction {i}"
    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)
    previous_block = new_block
block_data = {
    'Index': [block.index for block in blockchain],
    'Timestamp': [block.timestamp for block in blockchain],
    'Data': [block.data for block in blockchain],
}

df_blocks = pd.DataFrame(block_data)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Index', y='Timestamp', hue='Data', data=df_blocks, palette='viridis', s=100)
for i, txt in enumerate(df_blocks['Data']):
    plt.annotate(txt, (df_blocks['Index'][i], df_blocks['Timestamp'][i]), textcoords="offset points", xytext=(0,10), ha='center')
plt.title('Blockchain Visualization')
plt.xlabel('Block Index')
plt.ylabel('Timestamp')
plt.legend(title='Transactions', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.tight_layout()
plt.show()
