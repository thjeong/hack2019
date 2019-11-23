import random
import numpy as np
import pandas as pd
import datetime


def genSHBAccountTrans(seed, amt=5000, max_n_of_trans_digit = 2):
    """
    은행거래내역 dummy data 생성기
    :param seed:
    :param amt:
    :return:
    """
    random.seed(seed)
    random_number = random.random()
    n_of_trans = int(random_number*(10**max_n_of_trans_digit))
    list_of_text = ['blah1','blah2','blah3','blah4','blah5','blah6','blah7','급여','급여','급여']
    output_list = []
    for i in range(n_of_trans):
        text_data = list_of_text[int(np.mod(int(random_number * i),10))]
        if text_data == '급여':
            inout_idx = 1
            in_amt, out_amt = amt*1000, 0
        else:
            inout_idx = int(np.mod(int(random_number * (10 ** i)), 2))  # 입지구분 0 or 1
            if inout_idx ==1:
                in_amt, out_amt = amt, 0
            else:
                in_amt, out_amt = 0,amt

        output_list.append([str(inout_idx), in_amt, out_amt, text_data,''])
    return pd.DataFrame(output_list,columns=['입지구분','입금','출금','적요','거래점'])

def genAdditionalSHCTrans(input_aprvamt, cardno, n_of_trans, userid):
    """

    :param seed:
    :param input_aprvamt:
    :param cardno:
    :param aprv_date:
    :return:
    """
    list_of_mct_nm = ['이마트왕십리', '현대그린푸드', '가야성', '장칼국수', '보건옥', '만족오향족발', '카페드비반트',
                      '호반집', '주식회사스타필드하남', '남해바다', '알촌한양대점', '라화쿵부명동2호점']
    output_list = []
    for i in range(n_of_trans):
        random.seed('{}{}'.format(i, userid))
        random_number = random.random()
        current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        aprvno = '{:08d}'.format(int(random_number*1000000))
        aprvamt = input_aprvamt * int(random_number*10)
        retlno = '{:010d}'.format(int(random_number * 1000000))
        retlname = list_of_mct_nm[int(np.mod(int(random_number * 100), len(list_of_mct_nm)))]
        debit_TF = divmod(int(random_number*10), 2)[1]
        if debit_TF == 0 : cr_db = '신용'
        else: cr_db = '체크'
        output_list.append([current_time, aprvno, aprvamt, cardno, retlno, retlname, cr_db])
    output_list.reverse()
    output_df = pd.DataFrame(output_list,
                             columns=['승인일시', '승인번호', '승인금액', '카드뒷세자리', '가맹점번호', '가맹점명', '구분'])
    return output_df


def genSHCTrans(seed, input_aprvamt, cardno, stt_date, end_date, max_n_of_trans_digit = 3):
    """
    신용카드 국내사용내역조회 dummy data 생성
    :param seed:
    :param input_aprvamt:
    :param stt_date:
    :param end_date:
    :param max_n_of_trans_digit:
    :return: end_date=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d')
    """
    random.seed(seed+stt_date+end_date)
    random_number = random.random()
    n_of_trans = int(random_number*(10**max_n_of_trans_digit))
    list_of_mct_nm = ['이마트왕십리','현대그린푸드','신한생명','가야성','장칼국수','보건옥','지방세','서울버스','서울지하철','XX전통시장',
                      '만족오향족발','카페드비반트','호반집','주식회사스타필드하남','남해바다','알촌한양대점','라화쿵부명동2호점','XX도서']
    output_list = []
    date_idx = 0
    for i in range(n_of_trans):
        aprvdate = (datetime.datetime.strptime(stt_date,"%Y%m%d") + datetime.timedelta(days=date_idx)).strftime("%Y%m%d")
        if aprvdate == end_date: # 마지막날짜보다 뒤로 가면 그냥 거래일자는 end date과 동일하게 세
            date_idx = 0
        else:
            date_idx += 1
        aprvtime = aprvdate + '{:06d}'.format(i)
        aprvno = '{:08d}'.format(i)[:8]
        aprvamt = int(input_aprvamt / (int(np.mod(int(random_number * i),2))+1))
        retlno = '{:010d}'.format(i)[:10]
        retlname = list_of_mct_nm[int(np.mod(int(random_number * i * 100), len(list_of_mct_nm)))]
        output_list.append([aprvtime,aprvno,aprvamt,cardno,retlno,retlname])
    return pd.DataFrame(output_list,columns=['승인일시','승인번호','승인금액','카드뒷세자리','가맹점번호','가맹점명'])


def genSHDTrans(seed, input_aprvamt, cardno, stt_date, end_date, max_n_of_trans_digit = 3):
    """
    체크카드 국내사용내역조회 dummy data 생성
    :param seed:
    :param input_aprvamt:
    :param stt_date:
    :param end_date:
    :param max_n_of_trans_digit:
    :return:
    """
    random.seed(end_date+seed+stt_date)
    random_number = random.random()
    n_of_trans = int(random_number*(10**max_n_of_trans_digit))
    list_of_mct_nm = ['서울버스','서울지하철','XX전통시장','XX도서','신한생명','보건옥','가야성','장칼국수','이마트왕십리','현대그린푸드',
                      '맥도날드명동점','GS25 나라키움점','아재커피지로2가점','을지 쭈꾸미','교대이층집','토상막회','리틀사이공','지방세']
    output_list = []
    date_idx = 0
    for i in range(n_of_trans):
        aprvdate = (datetime.datetime.strptime(stt_date,"%Y%m%d") + datetime.timedelta(days=date_idx)).strftime("%Y%m%d")
        if aprvdate == end_date: # 마지막날짜보다 뒤로 가면 그냥 거래일자는 end date과 동일하게 세
            date_idx = 0
        else:
            date_idx += 1
        aprvtime = aprvdate + '{:06d}'.format(i)
        aprvno = '{:08d}'.format(i)[:8]
        aprvamt = int(input_aprvamt / (int(np.mod(int(random_number * i),2))+1))
        retlno = '{:010d}'.format(i)[:10]
        retlname = list_of_mct_nm[int(np.mod(int(random_number * i * 100), len(list_of_mct_nm)))]
        output_list.append([aprvtime,aprvno,aprvamt,cardno,retlno,retlname])
    return pd.DataFrame(output_list, columns=['승인일시', '승인번호', '승인금액', '카드뒷세자리', '가맹점번호', '가맹점명'])


def genSHCBill(seed, input_aprvamt, cardno, stt_date, end_date, max_n_of_trans_digit = 3):
    """
    (신용)월별청구내역조회(상세총괄) dummy data 생성
    :param seed:
    :param input_aprvamt:
    :param stt_date:
    :param end_date:
    :param max_n_of_trans_digit:
    :return:
    """
    random.seed(seed)
    random_number = random.random()
    df = genSHCTrans(seed, input_aprvamt, cardno, stt_date, end_date, max_n_of_trans_digit)
    df['적립예정포인트율'] = 0.001 * int(random_number * 10 + 1)
    df['청구원금금액'] = (df['승인금액'] * (1-df['적립예정포인트율']*1.2)).astype(int)
    df['매출일자'] = df['승인일시'].str[:8]
    del df['승인일시'], df['가맹점번호'], df['승인번호']
    df.rename(columns={'승인금액': '매출전표금액', '가맹점명': '이용가맹점명', '카드뒷세자리': '이용카드뒷세자리'}, inplace=True)
    return df

def genSHBhousesaving(seed):
    """
    10만원 이상 ~ 100만원 이하 1만원 단위로 random return
    :param seed:
    :return:
    """
    random.seed(seed)
    random_number = random.random()
    return int(round(random_number * 1000000, -4))


def genUserNm(userid):
    userid_dict = {'user2': '오상혁', 'user3': '정태환', 'user4': '이정은'}
    return userid_dict.get(userid)

def testRandom(seed):
    random.seed(seed)
    return random.random()