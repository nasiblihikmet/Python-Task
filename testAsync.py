import csv
import datetime
import asyncio
from web3 import Web3, AsyncHTTPProvider, HTTPProvider
import pandas as pd
from web3.middleware import geth_poa_middleware
import requests
from decimal import Decimal
from web3.exceptions import BlockNotFound
import json




provider_url = "https://lb.drpc.org/ogrpc?network=scroll&dkey=AkCtMlosOku5jbAYIluLoZIpI_vJSaoR77NivmJKmvm9"
web3 = Web3(HTTPProvider(provider_url))


contract_abi = '''
    [{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_weth","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"UNSAFE_swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bool","name":"stable","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"name":"getReserves","outputs":[{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"pair","type":"address"}],"name":"isPair","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"name":"pairFor","outputs":[{"internalType":"address","name":"pair","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"}],"name":"quoteAddLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"name":"quoteRemoveLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"sortTokens","outputs":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"components":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"stable","type":"bool"}],"internalType":"struct Router.route[]","name":"routes","type":"tuple[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address","name":"tokenFrom","type":"address"},{"internalType":"address","name":"tokenTo","type":"address"},{"internalType":"bool","name":"stable","type":"bool"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSimple","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"weth","outputs":[{"internalType":"contract IWETH","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]
'''
# Skydrome Contract address
contract_address = web3.to_checksum_address("0x03290a52ba3164639067622e20b90857eaded299")
print(contract_address)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


web3.middleware_onion.inject(geth_poa_middleware, layer=0)

async def find_transactions(web3, contract_address, start_block, end_block):
    contract_address = Web3.to_checksum_address(contract_address)
    transactions = []

    async def check_block(block_number):
        try:
            print(f"Checking block {block_number}")
            block = web3.eth.get_block(block_number, full_transactions=True)
            for tx in block['transactions']:
                if tx['from'] == contract_address or tx['to'] == contract_address:
                    transactions.append(tx)
        except BlockNotFound:
            print(f"Block {block_number} not found")

    tasks = [check_block(block_number) for block_number in range(start_block, end_block + 1)]
    await asyncio.gather(*tasks)

    return transactions


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

def get_block_number(timestamp):
    # return web3.eth.get_block(timestamp)['number']
    block = get_block_by_timestamp(web3, timestamp)
    return block['number']

# Calculate the timestamp for 24 hours ago and 30 days ago
now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=1)

async def main():
    start_block = 7938715
    end_block = 7938728
    
    transactions_arr = []
    address= set()
    amount = 0
    buyers_24h = set()
    sellers_24h = set()
    # Get trading events
    transactions = await find_transactions(web3, contract_address, start_block, end_block)
    print(transactions)
    for transaction in transactions:
        # address.add(transaction.seller_address)
        address.add(transaction["from"])
        # address.add(transaction.to)
        address.add(transaction['to'])
        # amount += transaction.amount
        amount += transaction['value']
        
           # Extract and format data according to the new headers
        block_hash = Web3.to_hex(transaction.get('blockHash', b''))
        block_number = transaction.get('blockNumber', 'N/A')
        from_address = Web3.to_checksum_address(transaction.get('from', 'N/A'))
        gas = transaction.get('gas', 'N/A')
        gas_price = transaction.get('gasPrice', 'N/A')
        max_fee_per_gas = transaction.get('maxFeePerGas', 'N/A')
        max_priority_fee_per_gas = transaction.get('maxPriorityFeePerGas', 'N/A')
        tx_hash = Web3.to_hex(transaction.get('hash', b''))
        input_data = Web3.to_hex(transaction.get('input', b''))
        nonce = transaction.get('nonce', 'N/A')
        to_address = Web3.to_checksum_address(transaction.get('to', 'N/A'))
        transaction_index = transaction.get('transactionIndex', 'N/A')
        value = Web3.from_wei(transaction.get('value', 0), 'ether')
        tx_type = transaction.get('type', 'N/A')
        access_list = json.dumps(transaction.get('accessList', 'N/A'))  # Convert lists to JSON strings
        chain_id = transaction.get('chainId', 'N/A')
        v = transaction.get('v', 'N/A')
        r = Web3.to_hex(transaction.get('r', b''))
        s = Web3.to_hex(transaction.get('s', b''))

        transactions_arr.append([
            block_hash,
            block_number,
            from_address,
            gas,
            gas_price,
            max_fee_per_gas,
            max_priority_fee_per_gas,
            tx_hash,
            input_data,
            nonce,
            to_address,
            transaction_index,
            value,
            tx_type,
            access_list,
            chain_id,
            v,
            r,
            s
        ])
        
        buyers_24h.add(transaction['to'])
        sellers_24h.add(transaction['from'])

    total_trading_volume_eth = web3.from_wei(amount, 'ether')
    print(f"Total Trading Volume in 24 hours: {total_trading_volume_eth} ETH")

    print("List of addresses that bought in the last 24 hours:")
    print(list(buyers_24h))

    print("List of addresses that sold in the last 24 hours:")
    print(list(sellers_24h))

    with open('skydrome_trading_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Addresses that bought SKY in the last 24 hours'])
        writer.writerow(list(buyers_24h))
        writer.writerow(['Addresses that sold SKY in the last 24 hours'])
        writer.writerow(list(sellers_24h))
        # writer.writerow(['Addresses Transcations'])
        # writer.writerow(transactions_arr)

  # Write transactions data
       
        writer.writerow([
            'Block Hash', 'Block Number', 'From', 'Gas', 'Gas Price', 'Max Fee Per Gas',
            'Max Priority Fee Per Gas', 'Hash', 'Input', 'Nonce', 'To', 'Transaction Index',
            'Value', 'Type', 'Access List', 'Chain ID', 'V', 'R', 'S'
        ])
        
        for tx in transactions_arr:
            writer.writerow(tx)

        # writer.writerow(['Transactions (from, to, value, hash)'])
        # for tx in transaction_set:
        #     writer.writerow(tx)

        # writer.writerow(['Block Hash', 'Block Number', 'From', 'Gas', 'Gas Price', 'Max Fee Per Gas',
        #     'Max Priority Fee Per Gas', 'Hash', 'Input', 'Nonce', 'To', 'Transaction Index',
        #     'Value', 'Type', 'Access List', 'Chain ID', 'V', 'R', 'S'])
        # for transaction_tuple in transaction_set:
        #  writer.writerow(list(transaction_tuple))
        


if __name__ == "__main__":
    asyncio.run(main())




    # # Save data to CSV
# with open('skydrome_trading_data.csv', mode='w') as file:
#     writer = csv.writer(file)
#     # writer.writerow(['Number of addresses that traded SKY in the last 24 hours', len(unique_address_count)])
#     # writer.writerow(['Total SKY Trading Volume in 24 hours in USD', total_trading_volume_usd])
#     # writer.writerow(['Total SKY Trading Volume in 30 days in USD', total_trading_volume_usd_30d])
#     writer.writerow(['Addresses that bought SKY in the last 24 hours'] + list(buyers_24h))
#     writer.writerow(['Addresses that sold SKY in the last 24 hours'] + list(sellers_24h))

