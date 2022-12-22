import matplotlib.pyplot as plt
import numpy as np
import requests
import json

data_json = requests.get("http://172.16.2.9:5000/get").json()

for (time,value) in json.loads(str(data_json)).items():
    print(time,value)