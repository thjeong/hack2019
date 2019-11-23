import requests, json
shbIP = 'http://10.3.17.61:8080' # 신한은행
shcIP = 'http://10.3.17.61:8081' # 신한카드
shiIP = 'http://10.3.17.61:8082' # 신한금투
shlIP = 'http://10.3.17.61:8083' # 신한생명

def tmp_api_func(ip, uri, data):
    """
    :param ip: 그룹사 IP
    :param uri:
    :param data:
    :return:
    """
    res = requests.post(ip + uri, data=json.dumps(data))
    return res.json()