import json
import pandas as pd
import datetime
from server.genDummyData import *
from server.taxFunctions import *
from server.api_request import *

def login_func(userid, year='2018'):
    """
    user id 받아서 전년도 급여내역 정리해서 알려주기
    :param userid:
    :return:
    """
    # 고객 계좌리스트 API 호출 & 계좌리스트로 거래내역 API호출 & 가라데이터 만들어 붙이기
    account_no_list = shbAccountList(userid)
    shb_trans_df = shbAccountTrans(account_no_list, year+'0101', year+'1231')
    shb_trans_df = pd.concat([shb_trans_df, genSHBAccountTrans(userid)])
    net_income = shb_trans_df[shb_trans_df['적요'].str.contains('급여')]['입금'].sum()
    total_salary = simple_tax_calc(net_income, 'server/data/')
    output_json = json.dumps({'userid' : userid, 'username': genUserNm(userid), 'total_salary': total_salary})
    return output_json


def summary_func(userid, total_salary, stt_date='20190101',
                 end_date=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d')):
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

    #신용,체크카드이용내역 API호출 & 가라데이터 만들어붙이기
    crd_card_df = shcSearchUseforDomestic(stt_date, end_date, debitTF=0)
    input_aprvamt = int(crd_card_df['승인금액'][0])
    cardno = crd_card_df['카드뒷세자리'][0]
    crd_card_df = pd.concat([crd_card_df, genSHCTrans(userid, input_aprvamt, cardno, stt_date, end_date)])

    deb_card_df = shcSearchUseforDomestic(stt_date, end_date, debitTF=1)
    input_aprvamt = int(deb_card_df['승인금액'][0])
    cardno = deb_card_df['카드뒷세자리'][0]
    deb_card_df = pd.concat([deb_card_df, genSHDTrans(userid, input_aprvamt, cardno, stt_date, end_date)])

    # 공제대상 제외거래 빼기(원래는 가맹점번호리스트, 혹은 업종으로 걸러내야 하지만, 제공 api데이터에 업종정보가 없음)
    crd_card_use = crd_card_df[~crd_card_df['가맹점명'].str.contains('지방세|세금|상품권')]['승인금액'].sum()
    deb_card_use = deb_card_df[~deb_card_df['가맹점명'].str.contains('지방세|세금|상품권')]['승인금액'].sum()

    # 대중교통, 전통시장, 도서/공연 이용금액(원래는 가맹점번호리스트, 혹은 업종으로 걸러내야 하지만, 제공 api데이터에 업종정보가 없음)
    public_trans_use = crd_card_df[crd_card_df['가맹점명'].str.contains('버스|지하철')]['승인금액'].sum()\
                           + deb_card_df[deb_card_df['가맹점명'].str.contains('버스|지하철')]['승인금액'].sum()
    trad_market_use = crd_card_df[crd_card_df['가맹점명'].str.contains('전통시장')]['승인금액'].sum()\
                          + deb_card_df[deb_card_df['가맹점명'].str.contains('전통시장')]['승인금액'].sum()
    book_use = crd_card_df[crd_card_df['가맹점명'].str.contains('도서')]['승인금액'].sum()\
                   + deb_card_df[deb_card_df['가맹점명'].str.contains('도서')]['승인금액'].sum()

    crd_etc_deduce, trad_market_deduce, \
    public_trans_deduce, book_show_deduce, \
    dummy1, dummy2, dummy3 = getCreditCrdEtcDeduction(crd_card_use, deb_card_use, 0, trad_market_use, public_trans_use,
                                                      book_use, total_salary)
    # 주택청약저축
    # 고객 계좌리스트 API호출 & 계좌리스트로 예적금 API호출(주택청약저축 금액) & 가라데이터 만들어 붙이기
    account_no_list = shbAccountList(userid)
    house_saving = shbDepositInstallmentDetail(account_no_list, stt_date, end_date)
    house_saving += genSHBhousesaving(userid)
    house_saving_deduce = getHouseSaving(house_saving, total_salary)

    output_dict = {'userid': userid,
                   'username': genUserNm(userid),
                   'total_salary': total_salary,
                   'earned_income_deduce': earned_income_deduce,
                   'n_of_members': 1, # 인적공제대상 인원 default 1
                   'personal_allowance_deduce': personal_allowance,
                   'pension_insurance_deduce': pension_insurance_deduce,
                   'spec_income_deduce': spec_income_deduce,
                   'crd_card_use': int(crd_card_use), 'deb_card_use': int(deb_card_use), 'cash_use': 0,
                   'crd_etc_use_amt': int(crd_card_use + deb_card_use),
                   'crd_etc_deduce': crd_etc_deduce,
                   'crd_etc_deduce_hurdle': int(total_salary * 0.25),
                   'public_trans_use': int(public_trans_use),
                   'public_trans_deduce': public_trans_deduce,
                   'trad_market_use': int(trad_market_use),
                   'trad_market_deduce': trad_market_deduce,
                   'book_use': int(book_use), 'book_deduce': book_show_deduce,
                   'house_saving': house_saving, 'householder_tf': 0, 'house_saving_deduce': house_saving_deduce,
                   'my_stock': 0, 'my_stock_deduce': 0, 'etc_deduce': 0}
    total_deduce = 0
    for i, j in output_dict.items():
        if i.endswith('deduce'):
            total_deduce += j
    output_dict['total_deduce'] = total_deduce
    return json.dumps(output_dict)


def detail_func(input_json, stt_date='20190101',
                end_date=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d'), unit_amt=10000):
    """
    ㅇㅇㅇㅇㅇㅇ
    :param input_json:
    :param stt_date:
    :param end_date:
    :return:
    """
    #input_dict = json.loads(input_json)
    input_dict = input_json
    userid, total_salary, n_of_members = input_dict['userid'], input_dict['total_salary'], input_dict['n_of_members']
    crd_card_use, deb_card_use, cash_use = input_dict['crd_card_use'], input_dict['deb_card_use'], input_dict['cash_use']
    public_trans_use = input_dict['public_trans_use']
    trad_market_use = input_dict['trad_market_use']
    book_use = input_dict['book_use']
    house_saving = input_dict['house_saving']
    householder_tf = input_dict['householder_tf']
    my_stock = input_dict['my_stock']
    etc_deduce = input_dict['etc_deduce']

    # 근로소득공제금액
    earned_income_deduce = getEarnedIncomeDeduction(total_salary)
    # 인적공제금액
    personal_allowance = getPersonalAllowance(n_of_members)
    #연금보험료공제
    pension_insurance_deduce = input_dict['pension_insurance_deduce']
    #특별소득공제
    spec_income_deduce = input_dict['spec_income_deduce']

    if input_dict.get('req_add_trans') != None:
        add_trans_df = genAdditionalSHCTrans(unit_amt, '312', input_dict.get('req_add_trans'), userid)
        crd_card_use += int(add_trans_df[add_trans_df['구분'] == '신용']['승인금액'].sum())
        deb_card_use += int(add_trans_df[add_trans_df['구분'] == '체크']['승인금액'].sum())


    crd_etc_use_amt = crd_card_use + deb_card_use + cash_use
    hurdle = total_salary * 0.25
    crd_etc_deduce, trad_market_deduce, \
    public_trans_deduce, book_show_deduce, \
    crd_card_deduce_valid_amt, \
    deb_cash_deduce_valid_amt,  \
    crd_etc_deduction_limit= getCreditCrdEtcDeduction(crd_card_use, deb_card_use, cash_use, trad_market_use,
                                                      public_trans_use, book_use, total_salary)
    # 주택청약저축
    house_saving_deduce = getHouseSaving(house_saving, total_salary, householder_tf)
    # 우리사주
    my_stock_deduce = getMyStock(my_stock)

    output_dict = {'userid': userid,
                   'username': genUserNm(userid),
                   'total_salary': total_salary,
                   'earned_income_deduce': earned_income_deduce,
                   'n_of_members': n_of_members,
                   'personal_allowance_deduce': personal_allowance,
                   'pension_insurance_deduce': pension_insurance_deduce,
                   'spec_income_deduce': spec_income_deduce,
                   'crd_card_use': int(crd_card_use), 'deb_card_use': int(deb_card_use), 'cash_use': cash_use,
                   'crd_etc_use_amt': int(crd_etc_use_amt),
                   'crd_card_deduce_valid_amt': crd_card_deduce_valid_amt,
                   'deb_cash_deduce_valid_amt': deb_cash_deduce_valid_amt,
                   'crd_etc_deduce': crd_etc_deduce,
                   'crd_etc_deduce_hurdle': int(hurdle), 'crd_etc_deduction_limit': crd_etc_deduction_limit,
                   'public_trans_use': int(public_trans_use),
                   'public_trans_deduce': public_trans_deduce,
                   'trad_market_use': int(trad_market_use),
                   'trad_market_deduce': trad_market_deduce,
                   'book_use': int(book_use), 'book_deduce': book_show_deduce,
                   'house_saving': house_saving, 'householder_tf': householder_tf,
                   'house_saving_deduce': house_saving_deduce,
                   'my_stock': my_stock, 'my_stock_deduce' : my_stock_deduce,
                   'etc_deduce': etc_deduce}
    total_deduce = 0
    for i, j in output_dict.items():
        if i.endswith('deduce'):
            total_deduce += j
    output_dict['total_deduce'] = total_deduce

    # 현재 소득공제 현황 내용 만들기
    std_assessment = total_salary - total_deduce
    tax_amt, acc_tax_ratio, txt_msg, max_ratio_amt, max_ratio = getTax(std_assessment)
    output_dict['std_assessment'] = std_assessment
    output_dict['tax_amt'] = tax_amt
    output_dict['acc_tax_ratio'] = acc_tax_ratio
    output_dict['txt_msg'] = txt_msg
    output_dict['max_ratio'] = max_ratio

    # 신용체크현금소득공제 상세현황 만들기
    hurdle_ramains = hurdle - crd_etc_use_amt  # 허들 넘기까지 남은 금액
    output_dict['hurdle_remains'] = hurdle_ramains
    result = getBenefitPerUsage(userid, max_ratio, crd_card_use, deb_card_use, cash_use, total_salary,
                                crd_etc_deduction_limit, crd_etc_deduce, unit_amt)
    output_dict['crd_tax_benefit'] = result[0]
    output_dict['deb_cash_tax_benefit'] = result[1]
    output_dict['crd_benefit'] = result[2]
    output_dict['crd_benefit_ratio'] = result[3]
    output_dict['crd_benefit_sum'] = result[4]
    output_dict['deb_benefit'] = result[5]
    output_dict['deb_benefit_ratio'] = result[6]
    output_dict['deb_cash_benefit_sum'] = result[7]

    # 카드이용전략메세지 만들기
    if hurdle_ramains > 0:
        crd_etc_strategy = '각종 혜택이 많은 신용카드로 소득공제 문턱을 넘어보세요!'
        hurdle_info_msg = '소득공제 최소 문턱(연봉 25%)를 넘기까지 {}원 남았습니다.'.format(getInsertComma(int(hurdle_ramains)))
    elif crd_etc_deduce >= crd_etc_deduction_limit: # 소득공제금액이 소득공제 한도를 넘었을 때
        crd_etc_strategy = '각종 혜택이 많은 신용카드를 사용하시는 게 좋습니다.'
        hurdle_info_msg = '신용체크현금 항목의 소득공제 금액이 이미 한도({}원)를 채웠습니다.'.format(getInsertComma(int(crd_etc_deduction_limit)))
    elif output_dict['crd_benefit_sum'] >= output_dict['deb_cash_benefit_sum']: # 신용카드혜택 > 체크현금혜택
        crd_etc_strategy = '신용카드와 체크/현금 중, 기대 혜택이 더 큰 신용카드를 이용 하시면 좋습니다!'
        hurdle_info_msg = '소득공제 최소 문턱(연봉 25%)을 넘었습니다!'
    else:
        crd_etc_strategy = '신용카드와 체크/현금 중, 기대 혜택이 더 큰 체크카드를 이용하시면 좋습니다!'
        hurdle_info_msg = '소득공제 최소 문턱(연봉 25%)을 넘었습니다!'
    output_dict['crd_etc_strategy'] = crd_etc_strategy
    output_dict['hurdle_info_msg'] = hurdle_info_msg

    # 최근 신용, 체크 카드이용내역 만들기
    crd_card_df = shcSearchUseforDomestic(stt_date, end_date, debitTF=0)
    input_aprvamt = int(crd_card_df['승인금액'][0])
    cardno = crd_card_df['카드뒷세자리'][0]
    crd_card_df = pd.concat([crd_card_df, genSHCTrans(userid, input_aprvamt, cardno, stt_date, end_date)])

    deb_card_df = shcSearchUseforDomestic(stt_date, end_date, debitTF=1)
    input_aprvamt = int(deb_card_df['승인금액'][0])
    cardno = deb_card_df['카드뒷세자리'][0]
    deb_card_df = pd.concat([deb_card_df, genSHDTrans(userid, input_aprvamt, cardno, stt_date, end_date)])

    crd_card_df['구분'] = '신용'
    deb_card_df['구분'] = '체크'
    card_df = pd.concat([crd_card_df, deb_card_df]).sort_values('승인일시', ascending=False).reset_index(drop=True)

    if input_dict.get('req_add_trans') != None:
        # add_trans_df = genAdditionalSHCTrans(input_aprvamt, cardno, input_dict.get('req_add_trans'), userid)
        card_df = pd.concat([add_trans_df, card_df])

    # 공제대상 제외 혹은 별도한도 운영되는 거래 빼기(원래는 가맹점번호리스트, 혹은 업종으로 걸러내야 하지만, 제공 api데이터에 업종정보가 없음)
    card_df = card_df[~card_df['가맹점명'].str.contains('지방세|세금|상품권|버스|지하철|전통시장|도서')].reset_index(drop=True).head()
    crd_benefit_ratio = result[4] / 10000
    deb_cash_benefit_ratio = result[7] / 10000
    recent_crd_deb_use_list = []
    for row in card_df.iterrows():
        tmp_dict = {}
        tmp_dict['apv_d'] = '{}.{}'.format(row[1]['승인일시'][4:6], row[1]['승인일시'][6:8])
        tmp_dict['crd_tcd'] = row[1]['구분']
        tmp_dict['apv_amt'] = row[1]['승인금액']
        tmp_dict['mct_nm'] = row[1]['가맹점명']
        if row[1]['구분'] == '신용':
            tmp_dict['benefit'] = int(round(row[1]['승인금액']*crd_benefit_ratio))
        else:
            tmp_dict['benefit'] = int(round(row[1]['승인금액'] * deb_cash_benefit_ratio))
        if row[1]['승인일시'][:8] == datetime.datetime.now().strftime('%Y%m%d'):
            tmp_dict['new_trans_TF'] = 1
        else:
            tmp_dict['new_trans_TF'] = 0
        recent_crd_deb_use_list.append(tmp_dict)
    output_dict['recent_crd_deb_use_list'] = recent_crd_deb_use_list

    # 대중교통, 전통시장 소득공제 상세현황 만들기
    output_dict['public_trans_deduce_limit'] = 1000000
    output_dict['trad_market_deduce_limit'] = 1000000

    if crd_etc_use_amt >= hurdle and public_trans_deduce < 1000000:
        output_dict['public_trans_benefit'] = unit_amt * 0.4 * max_ratio
    else:
        output_dict['public_trans_benefit'] = 0
    if crd_etc_use_amt >= hurdle and trad_market_deduce < 1000000:
        output_dict['trad_market_benefit'] = unit_amt * 0.4 * max_ratio
    else:
        output_dict['trad_market_benefit'] = 0

    return json.dumps(output_dict)
