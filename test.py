# import requests

# # Define the base URL and parameters
# base_url = "https://api.scrollscan.com/api"
# params = {
#     "module": "account",
#     "action": "balancemulti",
#     "address": "0xaf8ae6955d07776ab690e565ba6fbc79b8de3a5d,0xe93685f3bba03016f02bd1828badd6195988d950",
#     "tag": "latest",
#     "apikey": "YourApiKeyToken"  # Replace with your actual API key
# }

# # Make the GET request
# response = requests.get(base_url, params=params)

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the JSON response
#     data = response.json()
#     print(data)
# else:
#     print(f"Error: {response.status_code}")
#     print(response.text)


# from web3 import Web3, EthereumTesterProvider
# w3 = Web3(EthereumTesterProvider())
# print(w3.is_connected())


# from web3 import Web3, HTTPProvider
          
# def test_block_number():
#     url = "https://scroll.drpc.org"  # url string
    
#     web3 = Web3(HTTPProvider(url))
#     print(web3.eth.block_number)

# test_block_number()