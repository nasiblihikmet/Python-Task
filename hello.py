import csv
import datetime
import pandas as pd
from web3 import Web3
from web3.middleware import geth_poa_middleware
import requests
from decimal import Decimal
import asyncio
from web3.exceptions import BlockNotFound

# Connect to Scroll Layer 2 network
# https://scroll.drpc.org

provider_url = ""
web3 = Web3(Web3.HTTPProvider(provider_url))

web3.middleware_onion.inject(geth_poa_middleware, layer=0)

 
# # Check if the connection is successful
# if web3.is_connected():
#     print("Connected to Scroll Layer 2 network")
# else:
#     print("Failed to connect to Scroll Layer 2 network")
#     exit(1)

# ABI for the Skydrome Contract (simplified, should be replaced with the actual ABI)
contract_abi = '''
    [{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_weth","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"UNSAFE_swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bool","name":"stable","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"name":"getReserves","outputs":[{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"pair","type":"address"}],"name":"isPair","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"name":"pairFor","outputs":[{"internalType":"address","name":"pair","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"}],"name":"quoteAddLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"name":"quoteRemoveLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"sortTokens","outputs":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address","name":"tokenFrom","type":"address"},{"internalType":"address","name":"tokenTo","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSimple","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"weth","outputs":[{"internalType":"contract IWETH","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]
'''
# Skydrome Contract address
contract_address = web3.to_checksum_address("")
print(contract_address)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

async def find_transactions(web3, contract_address, start_block, end_block):
    contract_address = Web3.to_checksum_address(contract_address)
    transactions = []

    async def check_block(block_number):
        try:
            print(f"Проверка блока {block_number}")
            block = await web3.eth.get_block(block_number, full_transactions=True)
            for tx in block['transactions']:
                if tx['from'] == contract_address or tx['to'] == contract_address:
                    transactions.append(tx)
        except BlockNotFound:
            print(f"Блок {block_number} не найден")

    tasks = [check_block(block_number) for block_number in range(start_block, end_block + 1)]
    await asyncio.gather(*tasks)

    return transactions

# Function to get events from the contract
def get_events(event_name, from_block, to_block):
    event_filter = contract.events.Transfer.createFilter(fromBlock=from_block, toBlock=to_block)
    return event_filter.get_all_entries()

# Calculate the timestamp for 24 hours ago and 30 days ago
now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=1)
thirty_days_ago = now - datetime.timedelta(days=30)

def get_block_by_timestamp(web3, timestamp):
    latest_block = web3.eth.get_block_number()              
    earliest_block = 0

    while earliest_block <= latest_block:
        mid_block = (earliest_block + latest_block) // 2
        block = web3.eth.get_block(mid_block)
        
        if block['timestamp'] < timestamp:
            earliest_block = mid_block + 1
        elif block['timestamp'] > timestamp:
            latest_block = mid_block - 1
        else:
            return block
        
    return web3.eth.get_block(earliest_block)

            
# Convert timestamps to block numbers
def get_block_number(timestamp):
    # return web3.eth.get_block(timestamp)['number']
    block = get_block_by_timestamp(web3, timestamp)
    return block['number']

current_block =  web3.eth.get_block_number()
yesterday_timestamp = int(yesterday.timestamp())
yesterday_block = get_block_number(yesterday_timestamp)
# thirty_days_ago_block = get_block_number(thirty_days_ago.timestamp())
thirty_days_ago_timestamp = int(thirty_days_ago.timestamp())
thirty_days_ago_block = get_block_number(thirty_days_ago_timestamp)



address= set()
amount = 0
amount_30d = 0
buyers_24h = set()
sellers_24h = set()
# Get trading events
transactions = find_transactions(contract_address, yesterday_block, current_block)
print(transactions)
for transaction in transactions:
    # address.add(transaction.seller_address)
    address.add(transaction["from"])
    # address.add(transaction.to)
    address.add(transaction['to'])
    # amount += transaction.amount
    amount += transaction['value']

    buyers_24h.add(transaction['to'])
    sellers_24h.add(transaction['from'])
   

    # Get trading events for the last 30 days
transactions_30d = find_transactions(contract_address, current_block-3, current_block)
for transaction in transactions_30d:
    amount_30d += transaction['value']

        # Number of unique addresses
unique_address_count = len(address)
print(f"Number of addresses that traded SKY in the last 24 hours: {unique_address_count}")

total_trading_volume_eth = web3.from_wei(amount, 'ether')
print(f"Total SKY Trading Volume in 24 hours: {total_trading_volume_eth} ETH")

print(len(address)) # Number of addresses that traded SKY in the last 24 hours
print(amount) # Total SKY Trading Volume in 24 hours in ETH >> convert USD

total_trading_volume_eth_30d = web3.from_wei(amount_30d, 'ether')
print(f"Total SKY Trading Volume in 30 days: {total_trading_volume_eth_30d} ETH")

def get_eth_price():
    response = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=ETH')
    data = response.json()
    eth_usd_rate = float(data['data']['rates']['USD'])
    return eth_usd_rate

eth_usd_rate = get_eth_price()
total_trading_volume_eth = Decimal(total_trading_volume_eth)
total_trading_volume_eth_30d = Decimal(total_trading_volume_eth_30d)
eth_usd_rate_decimal = Decimal(eth_usd_rate)

total_trading_volume_usd = total_trading_volume_eth * eth_usd_rate_decimal
print(f"Total SKY Trading Volume in 24 hours in USD: ${total_trading_volume_usd:.2f} USD") # Total SKY Trading Volume in 24 hours in USD

total_trading_volume_usd_30d = total_trading_volume_eth_30d * eth_usd_rate_decimal
print(f"Total SKY Trading Volume in 30 days in USD: ${total_trading_volume_usd_30d:.2f} USD")#Total SKY Trading Volume in 30 days in USD

print("List of addresses that bought SKY in the last 24 hours:")
print(list(buyers_24h))

print("List of addresses that sold SKY in the last 24 hours:")
print(list(sellers_24h))



