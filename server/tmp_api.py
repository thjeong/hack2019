import requests, json
import pandas as pd


def tmp_api_func(ip, uri, data):
    res = requests.post(ip + uri, data=json.dumps(data))
    return res