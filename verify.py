import gzip
import json

with gzip.open("./output/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d_157_500.json.gz") as file:
    print(json.loads(file.read())[0])
    