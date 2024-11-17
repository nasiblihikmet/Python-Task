import csv
import datetime 
from datetime import timezone, timedelta
from datetime import datetime
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from web3.exceptions import BlockNotFound
import requests
from decimal import Decimal
import asyncio

# write here url
provider_url = ""
web3 = Web3(HTTPProvider(provider_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract_abi = ''''''


contract_address = web3.to_checksum_address("")
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

async def find_transactions(web3, contract_address, start_block, end_block):
    contract_address = Web3.to_checksum_address(contract_address)
    transactions = []

    async def check_block(block_number):
        try:
            block = web3.eth.get_block(block_number, full_transactions=True)
            for tx in block['transactions']:
                
                if tx['from'] == contract_address or tx['to'] == contract_address:
                    tx= dict(tx)
                    tx['timestamp'] = block['timestamp']
                    receipt = web3.eth.get_transaction_receipt(tx['hash'])
                    tx['status'] = receipt['status']
                    tx['method'] = '""'
                    tx['errcode'] = '""'
                    tx['contractaddress '] = '""'  # suspicious
                    tx['gasUsed'] = receipt['gasUsed']
                    tx['gasPrice'] = tx['gasPrice']
                    tx['txnFee'] = tx['gasUsed'] * tx['gasPrice'] if 'gasUsed' in tx and 'gasPrice' in tx else 0
                    transactions.append(tx)
        except BlockNotFound:
            pass 

    tasks = [check_block(block_number) for block_number in range(start_block, end_block + 1)]
    await asyncio.gather(*tasks)
    return transactions

def decode_method(input_data):
     if not input_data or len(input_data) < 10:
        return "Unknown"
     if isinstance(input_data, bytes):
        input_data = Web3.to_hex(input_data)

     method_id = input_data[:10]  
     try:
        for item in contract.abi:
            if item.get('type') == 'function':
                method_signature = item['name'] + '(' + ','.join([param['type'] for param in item['inputs']]) + ')'
                if Web3.sha3(text=method_signature)[:10] == method_id:
                    return item['name']
     except Exception as e:
       
      return "Unknown"

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
    block = get_block_by_timestamp(web3, timestamp)
    return block['number']

def get_eth_to_usd():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    data = response.json()
    return Decimal(data['ethereum']['usd'])  

async def main():
    start_block = ""
    end_block = ""
    
    transactions_arr = []
    address= set()
    amount = 0
    buyers_24h = set()
    sellers_24h = set()

    transactions = await find_transactions(web3, contract_address, start_block, end_block)

    eth_to_usd = get_eth_to_usd() 

    for transaction in transactions:
        address.add(transaction["from"])       
        address.add(transaction['to'])     
        amount += transaction['value']
        value_in_ether = Web3.from_wei(transaction['value'], 'ether')
        txn_fee_ether = (Web3.from_wei(transaction['txnFee'], 'ether'))  # Decimal
        txn_fee_usd = txn_fee_ether * eth_to_usd
        amount += value_in_ether
        block_hash = Web3.to_hex(transaction.get('blockHash', b''))
        block_number = transaction.get('blockNumber', 'N/A')
        timestamp = transaction.get('timestamp', 0)
        
        txn_fee_usd = txn_fee_ether * eth_to_usd
        utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
        from_address = Web3.to_checksum_address(transaction.get('from', 'N/A'))
        to_address = Web3.to_checksum_address(transaction.get('to', 'N/A'))
        contractaddress = transaction.get('contractaddress', 'N/A')
        value_out = Web3.from_wei(transaction.get('', 0), 'ether')  # suspicious
        status = transaction.get('status', 'N/A')
        errcode = transaction.get('errcode', 'N/A')
        method = transaction.get('method', 'N/A')

        transactions_arr.append([
            block_hash,block_number, timestamp,  utc_datetime.isoformat(), from_address, to_address, contractaddress,value_in_ether,value_out,txn_fee_ether,txn_fee_usd,status,errcode,method])
        
        buyers_24h.add(transaction['to'])
        sellers_24h.add(transaction['from'])

    with open('skydrome_trading_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Block Hash', 'Block Number',  'timestamp', 'DateTime (UTC)', 'From', 'To', 'ContractAddress', 'Value_IN(ETH)', 'Value_OUT(ETH)','TxnFee(ETH)','TxnFee(USD)',
            'Status', 'ErrCode', 'Method'  
        ])
        
        for tx in transactions_arr:
            writer.writerow(tx)

if __name__ == "__main__":
    asyncio.run(main())