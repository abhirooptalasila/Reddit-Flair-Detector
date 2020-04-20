import requests
import os
import json
import string


url = 'http://localhost:5000/reqp'

input_url = "https://new.reddit.com/r/india/comments/fz3spn/people_are_just_opening_share_market_account_my/"

dict = {8:"Scheduled", 7:"Politics",5:"Photography",6:"Policy/Economy",3:"Food", 2:"Coronavirus",1:"Business/Finance",4:"Non-Political",9:"Science/Technology",10:"Sports",0:"AskIndia"}

input_title = input_url.split("/")
if input_title[-1].isalpha():
    id_val = input_title[-2]
else:
    id_val = input_title[-3]

data = {"title": str(id_val)}
raw = json.dumps(data)
r_r = json.loads(raw)

r = requests.post(url,json=r_r)
class_id = str(r.json()["class"])
class_id = dict.get(int(list(class_id)[1]))
print("Predicted Flair: "+str(class_id))