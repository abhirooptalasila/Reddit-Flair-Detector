import requests
import os
import json
import string


url = 'http://localhost:5000/automated_testing'

fin = open('sample.txt', 'r')
files = {'file': fin}
try:
    r = requests.post(url, files=files)
    print("Returned Values:\n"+str(r.json()))
finally:
    fin.close()
