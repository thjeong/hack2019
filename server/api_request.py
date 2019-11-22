import requests, json
import pandas as pd
shbIP = 'http://10.3.17.61:8080'
shcIP = 'http://10.3.17.61:8081'

def shcSearchUseforDomestic(stt_date, end_date):
    """
    (신용)국내이용내역조회
    :param stt_date:
    :param end_date:
    :return:
    """
    inqterm = stt_date + end_date
    uri = '/v1/usecreditcard/searchusefordomestic'
    data = {
        "dataHeader":{},
        "dataBody": {"nxtQyKey":"",
                     "inqterm":inqterm,
                     "bctag":"0"
                     }
    }
    res = requests.post(shcIP+uri, data= json.dumps(data))
    databody = res.json()['dataBody']['grp001']
    output_list = []
    for i in databody:
        aprvtime = i.get('aprvtime')
        aprvno = i.get('aprvno')
        aprvamt = int(i.get('aprvamt'))
        cardno = i.get('cardno')
        retlno = i.get('retlno')
        retlname = i.get('retlname')
        output_list.append([aprvtime,aprvno,aprvamt,cardno,retlno,retlname])
    return pd.DataFrame(output_list, columns=['승인일시','승인번호','승인금액','카드뒷세자리','가맹점번호','가맹점명'])
