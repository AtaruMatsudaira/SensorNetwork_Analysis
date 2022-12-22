import matplotlib.pyplot as plt
import numpy as np
import requests
import json

data_json = requests.get("http://172.16.2.9:5000/get").json()

formatted_dic = {float(data_str): mag for data_str,mag in data_json.items()}

formatted_dic = dict(( (data,mag) for data,mag in sorted(formatted_dic.items())))

x = formatted_dic.keys()

y = formatted_dic.values()

plt.plot(x, y)
plt.show()