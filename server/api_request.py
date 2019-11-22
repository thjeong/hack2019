import requests, json
import pandas as pd
shbIP = 'http://10.3.17.61:8080'
shcIP = 'http://10.3.17.61:8081'

def shbAccountList(ssn):
    """
    신한은행 계좌 조회
    :param ssn: 주민번호
    :return:
    """
    uri = '/v1/account/list'
    data = {"dataHeader": {},
            "dataBody": {"serviceCode": "C2010",
                         "거래구분": "9",
                         "계좌감추기여부":"1",
                         "보안계좌조회구분":"2",
                         "주민등록번호": ssn}
            }
    res = requests.post(shbIP + uri, data=json.dumps(data))
    databody = res.json()['dataBody']['예금내역']
    account_no_list = []
    for i in databody:
        account_no_list.append(i.get('계좌번호_MASK'))
    return account_no_list

def shbAccountTrans(account_no_list, stt_date, end_date):
    """
    신한은행 계좌 거래내역 조회
    :param account_no:
    :return:
    """
    uri = '/v1/search/transaction/history'
    output_list = []
    for acc_no in account_no_list:
        data = {"dataHeader": {},
                "dataBody": {"serviceCode":"D1110",
                             "정렬구분":"1",
                             "조회시작일":'{}.{}.{}'.format(stt_date[0:4],stt_date[4:6],stt_date[6:8]),
                             "조회종료일":'{}.{}.{}'.format(end_date[0:4],end_date[4:6],end_date[6:8]),
                             "계좌번호": acc_no}}
        res = requests.post(shbIP + uri, data=json.dumps(data))
        databody = res.json()['dataBody']['거래내역']
        for i in databody:
            try:
                input_amt = int(i.get('입금'))
            except:
                input_amt = 0
            try:
                output_amt = int(i.get('출금'))
            except:
                output_amt = 0
            output_list.append([i.get('입지구분'), input_amt, output_amt, i.get('적요'), i.get('거래점')])
    return pd.DataFrame(output_list,columns=['입지구분','입금','출금','적요','거래점'])

def shbDepositInstallmentDetail(acc_no_list, stt_date, end_date):
    """
    예적금계좌내역 / 계좌정보 상세조회
    :param acc_no_list: 계좌번호 리스트
    :return:
    """
    uri = '/v1/account/deposit/detail'
    housesaving_sum = 0
    for acc_no in acc_no_list:
        data = {"dataHeader": {}, "dataBody": {"serviceCode":"D1130",
                                               "정렬구분":"1",
                                               "조회시작일": stt_date,
                                               "조회종료일": end_date,
                                               "조회기간구분":"1",
                                               "은행구분": "1",
                                               "계좌번호": acc_no
                                              }}
        res = requests.post(shbIP + uri, data=json.dumps(data))
        tmp_dict = res.json()['dataBody']
        if '주택청약' in tmp_dict['계좌명']:
            for i in tmp_dict['거래내역']:
                housesaving_sum += int(i.get['입금'])
    return housesaving_sum


def shcSearchUseforDomestic(stt_date, end_date, debitTF):
    """
    (신용,체크)국내이용내역조회
    :param stt_date:
    :param end_date:
    :param debitTF: 신용이면 0, 체크면 1
    :return:
    """
    inqterm = stt_date + end_date
    if debitTF == 0:
        uri = '/v1/usecreditcard/searchusefordomestic'
    else:
        uri = '/v1/usedebitcard/searchusefordomestic'
    data = {"dataHeader": {}, "dataBody": {"nxtQyKey": "", "inqterm": inqterm, "bctag": "0"}}
    res = requests.post(shcIP+uri, data= json.dumps(data))
    databody = res.json()['dataBody']['grp001']
    output_list = []
    for i in databody:
        aprvtime = i.get('aprvtime')
        aprvno = i.get('aprvno')
        aprvamt = int(i.get('aprvamt'))
        if debitTF == 0:
            cardno = i.get('cardno')
        else:
            cardno = i.get('usecardno')
        retlno = i.get('retlno')
        retlname = i.get('retlname')
        output_list.append([aprvtime,aprvno,aprvamt,cardno,retlno,retlname])
    output_df = pd.DataFrame(output_list, columns=['승인일시','승인번호','승인금액','카드뒷세자리','가맹점번호','가맹점명'])
    return output_df
