import json
import datetime
from server.genDummyData import genSHBAccountTrans, genUserNm, genSHCTrans, genSHDTrans
from server.taxFunctions import *

def login_func(userid, year='2018'):
    """
    user id 받아서 전년도 급여내역 정리해서 알려주기
    :param userid:
    :return:
    """
    # TODO: 은행 계좌거내역 api 호출 & dataframe으로 parsing하는 모듈 추가
    amt = 5000
    shb_trans_df = genSHBAccountTrans(userid, amt)
    net_income = shb_trans_df[shb_trans_df['적요'].str.contains('급여')]['입금'].sum()
    total_salary = simple_tax_calc(net_income, 'server/data/')
    output_json = json.dumps({'userid' : userid, 'username': genUserNm(userid), 'total_salary': total_salary})
    return output_json


def incomeDeduction1(userid, total_salary, stt_date='20190101', end_date=datetime.datetime.now().strftime('%Y%m%d')):
    """
    근로소득공제금액, 인적공제금액(default 150만), 연금보험료공제, 특별소득공제,
    신용/체크/현금영수증 이용금액, 공제금액, 총급여25%문턱금
    대중교통 이용금액, 공제금액
    전통시장 이용금액, 공제금액
    도서/공연 이용금액, 공제금액
    주택청약저축 이용금액, 공제금액
    우리사주조합출연금 (default 0)
    기타 (default 0)
    :param userid:
    :param total_salary:
    :return:
    """
    # 근로소득공제금액
    earned_income_deduce = getEarnedIncomeDeduction(total_salary)
    # 인적공제금액
    personal_allowance = getPersonalAllowance(1)
    #연금보험료공제
    pension_insurance_deduce = getTmpPensionInsuranceDeduction(total_salary)
    #특별소득공제
    spec_income_deduce = getTmpSpecIncomeDeduction(total_salary, 1)

    #신용,체크카드이용내역
    # TODO: 신용,체크카드 이용내역 api 호출 & dataframe으로 parsing하는
    input_aprvamt= 5000
    crd_card_df = genSHCTrans(userid, input_aprvamt, stt_date, end_date)
    deb_card_df = genSHDTrans(userid, input_aprvamt, stt_date, end_date)
    # 공제대상 제외거래 빼기(원래는 가맹점번호리스트, 혹은 업종으로 걸러내야 하지만, 제공 api데이터에 업종정보가 없음)
    crd_card_use = crd_card_df[~crd_card_df['가맹점명'].str.contains('지방세|세금|상품권')]['승인금액'].sum()
    deb_card_use = deb_card_df[~deb_card_df['가맹점명'].str.contains('지방세|세금|상품권')]['승인금액'].sum()

    #대중교통, 전통시장, 도서/공연 이용금액(원래는 가맹점번호리스트, 혹은 업종으로 걸러내야 하지만, 제공 api데이터에 업종정보가 없음)
    public_trans_use = crd_card_df[crd_card_df['가맹점명'].str.contains('버스|지하철')]['승인금액'].sum()\
                           + deb_card_df[deb_card_df['가맹점명'].str.contains('버스|지하철')]['승인금액'].sum()
    trad_market_use = crd_card_df[crd_card_df['가맹점명'].str.contains('전통시장')]['승인금액'].sum()\
                          + deb_card_df[deb_card_df['가맹점명'].str.contains('전통시장')]['승인금액'].sum()
    book_use = crd_card_df[crd_card_df['가맹점명'].str.contains('도서')]['승인금액'].sum()\
                   + deb_card_df[deb_card_df['가맹점명'].str.contains('도서')]['승인금액'].sum()

    crd_etc_deduce, trad_market_deduce, \
    public_trans_deduce, book_show_deduce = getCreditCrdEtcDeduction(crd_card_use, deb_card_use, 0, trad_market_use,
                                                                     public_trans_use, book_use, total_salary)
    output_dict = {'earned_income_deduce': earned_income_deduce,
                   'personal_allowance': personal_allowance,
                   'pension_insurance_deduce': pension_insurance_deduce,
                   'spec_income_deduce': spec_income_deduce,
                   'crd_etc_use_amt': crd_card_use + deb_card_use,
                   'crd_etc_deduce': crd_etc_deduce,
                   'public_trans_use': public_trans_use,
                   'public_trans_deduce': public_trans_deduce,
                   'trad_market_use': trad_market_use,
                   'trad_market_deduce': trad_market_deduce,
                   'book_use': book_use,
                   'house_saving': 0, 'house_saving_deduce': 0,
                   'my_stock': 0, 'etc': 0}
    return json.dumps(output_dict)