url = '<https://api.etherscan.io/api>'
params = {
  'module': 'block',
  'action': 'getblocknobytime',
  'timestamp' : int(time.time() // 1),
  'closest': 'before',
  'apikey': API_KEY
}
r = requests.get(url, params=params)
json_data = json.loads(r.text)["result"]
LATEST_BLOCK = int(json_data)