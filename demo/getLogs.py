# API_KEY - Etherscan api key, you get one after registration
OPENSEA_CONTRACT = '0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b'
url = '<https://api.etherscan.io/api>'
params = {
  'module': 'logs',
  'action': 'getLogs',
  'fromBlock' : BLOCK_START,
  'toBlock': 'latest',
  'address': OPENSEA_CONTRACT,
  'apikey': API_KEY
}
r = requests.get(url, params=params)
json_data = json.loads(r.text)["result"]