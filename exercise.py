# def factorial(n):
#     result = 1
#     for i in range(1, n + 1):
#         result *= i
#         #  print(f"i={i}, result={result}") 
#     return result

# print(factorial(5))  # Expected output: 120


from web3 import Web3
import time
# Connect to the Ethereum node
infura_url = "YOUR_INFURA_URL"
web3 = Web3(Web3.HTTPProvider (infura_url))
# Check if connected
 if not web3. isConnected (:
print("Failed to connect to the
Ethereum node.") else:
print ("Connected to the Ethereum node. ")
# Calculate the timestamp for 30 days ago
days_ago = 30
seconds_in_a_day = 86400
timestamp_30_days_ago = int (time.time ()) -
(days_ago * seconds_in_a_day)
# Get the latest block number
Latest_block = web.eth.block_number
# Function to get the block number closest
# to a specific timestamp 
 def get_block_by_timestamp (timestamp) :
 start = 0

 end = latest_block
 while start <= end:
 
 mid = (start + end) // 2

 block = web3. eth.get_block(mid)
 
 block_time = block[' timestamp']
 if block_time ‹ timestamp:
  start = mid + 1
 elif block_ time › timestamp:
   end = mid - 1
 else:
     return mid
return end


#  Get the block number from 30 days ago
 block_number_30_days_ago =get_block_by_timestamp timestamp_30_days_ago)
# Fetch the block
 block_30_days_ago =web3.eth.get_block(block_number-_30_days_ago, full _transactions=True)
# Display the last transaction from that block
 if block_30_days_ago and 'transactions' in block_30_days_ago:
 last_transaction = block_30_days_agol ['transactions'][-1]
