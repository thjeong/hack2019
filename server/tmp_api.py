import requests, json
import pandas as pd
shbIP = 'http://10.3.17.61:8080'
shcIP = 'http://10.3.17.61:8081'


def tmp_api_func(ip, uri, data):
    res = requests.post(ip + uri, data=json.dumps(data))
    return res