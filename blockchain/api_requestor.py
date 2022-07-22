import requests

class ApiRequestor(object):
    def __init__(self, api_url):
        self.api_url = api_url
        print("Initializing ApiRequestor")
        
    def get(self, path, params={}):
        response = requests.get(self.api_url + path, params=params)
        return response.json()