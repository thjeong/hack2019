# 세후 급여액으로 (세전)총급여액 계산
from server.genDummyData import genSHCBill
from server.api_request import shcSearchMonthlyBillingDetail
import pandas as pd
import datetime

def simple_tax_calc(net_income, table_file_dir):
    """
    실수령액으로 연봉 (얼추)계산
    :param net_income:
    :param table_file_dir:
    :return:
    """
    import scipy.interpolate as spi
    import numpy as np
    import os
    import pandas as pd
    df = pd.read_csv(os.path.join(table_file_dir,'total_salary_table.tsv'),sep='\t')
    if net_income <=103751760: # 연봉 1.5억에 해당하는 실수령액
        x = np.array(df['실수령액'])
        y = np.array(df['연봉'])
        split_idx = np.where(y == 122000000)[0][0]
        if net_income >= x[split_idx]:
            x = x[split_idx:]
            y = y[split_idx:]
        else:
            x = x[:split_idx]
            y = y[:split_idx]
        ipo = spi.splrep(x, y, k=1)
        total_salary = spi.splev(net_income,ipo).max()
        # deduce_ratio = 1 - net_income / total_salary
    else:
        A = np.vstack([np.array(df['실수령액']), np.ones(len(df))]).T
        w = np.linalg.lstsq(A, np.array(df['공제비율']))[0]
        deduce_ratio = net_income * w[0] + w[1]
        total_salary = net_income / (1-deduce_ratio)
    return max(int(total_salary), 0)





# 총 급여액으로 근로소득공제금액 계산
def getEarnedIncomeDeduction(total_salary):
    """
    총 급여액으로 근로소득공제금액 계산
    :param total_salary: 총 급여(세전)
    :return: 근로소득공제금액
    """
    if total_salary <= 5000000: # 500만원 이하. 급여액의 70%
        return int(total_salary * 0.7)
    elif total_salary <= 15000000: # 500만원초과, 1500만원 이하
        return int(3500000 + (total_salary - 5000000) * 0.4)
    elif total_salary <= 45000000: # 1500만원 초과, 4500만원 이하
        return int(7500000 + (total_salary - 15000000) * 0.15)
    elif total_salary <= 100000000: # 4500만원 초과, 1억 이하
        return int(12000000 + (total_salary - 45000000) * 0.05)
    else: # 1억원 초과
        return int(14750000 + (total_salary - 100000000) * 0.02)

# 공제대상 가족수로 인적공제금액 계산
def getPersonalAllowance(n_of_members):
    """
    :param n_of_members: 본인 포함한 공제대상 인원
    :return:
    """
    return 1500000 * n_of_members

# 총급여액으로 연금보험공제금액 얼추 계산
def getTmpPensionInsuranceDeduction(total_salary):
    """
    근로소득 간이세액표 산출 방법으로 임시 계산한것...
    :param total_salary:
    :return:
    """
    if total_salary/12 <= 290000:
        return 156600 # 290000 * 0.045 * 12
    elif total_salary/12 >= 4490000:
        return 2424600 # 4490000 * 0.045 * 12
    return int(total_salary * 0.045)

# 총급여액과 공제대상자 수로 특별소득공제 얼추 계산
def getTmpSpecIncomeDeduction(total_salary, n_of_members):
    """
    공제대상자는 1명 이상
    :param total_salary:
    :param n_of_members:
    :return:
    """
    if total_salary <= 30000000:
        if n_of_members == 1:
            return int(3100000 + total_salary * 0.04)
        elif n_of_members == 2:
            return int(3600000 + total_salary * 0.04)
        else:
            return int(5000000 + total_salary * 0.07 + max(total_salary - 40000000, 0) * 0.04)
    elif total_salary <= 45000000:
        if n_of_members == 1:
            return int(3100000 + total_salary * 0.04 - (total_salary - 30000000) * 0.05)
        elif n_of_members == 2:
            return int(3600000 + total_salary * 0.04 - (total_salary - 30000000) * 0.05)
        else:
            return int(5000000 + total_salary * 0.07 - (total_salary - 30000000) * 0.05 \
                   + max(total_salary - 40000000, 0) * 0.04)
    elif total_salary <= 70000000:
        if n_of_members == 1:
            return int(3100000 + total_salary * 0.015)
        elif n_of_members == 2:
            return int(3600000 + total_salary * 0.02)
        else:
            return int(5000000 + total_salary * 0.05 + (total_salary - 40000000) * 0.04)
    else:
        if n_of_members == 1:
            return int(3100000 + total_salary * 0.005)
        elif n_of_members == 2:
            return int(3600000 + total_salary * 0.01)
        else:
            return int(5000000 + total_salary * 0.03 + (total_salary - 40000000) * 0.04)


# 과세표준금액으로 산출세액 계산
def getTax(std_assessment):
    """
    과세표준금액으로 산출세액 계산
    :param std_assessment: 과표금액
    :return tax_amt: 산출세액
    :return acc_tax_ratio : 누적세율
    :return txt_msg : 텍스트 메세지
    :return max_ratio_amt : 최고세율 적용금액
    :return max_ratio : 최고세율
    """
    if std_assessment <= 12000000: # 1200만원 이하구간
        txt_msg = '1,200만원 이하 구간'
        max_ratio_amt, max_ratio = std_assessment, 0.06
        tax_amt = max_ratio_amt * max_ratio
    elif std_assessment <= 46000000:
        txt_msg = '1,200만원 초과, 4,600만원 이하 구간'
        max_ratio_amt, max_ratio = std_assessment - 12000000, 0.15
        tax_amt = 720000 + max_ratio_amt * max_ratio
    elif std_assessment <= 88000000:
        txt_msg = '4,600만원 초과, 8,800만원 이하 구간'
        max_ratio_amt, max_ratio = std_assessment - 46000000, 0.24
        tax_amt = 5820000 + max_ratio_amt * max_ratio
    elif std_assessment <= 150000000:
        txt_msg = '8,800만원 초과, 1억5천만원 이하 구간'
        max_ratio_amt, max_ratio = std_assessment - 88000000, 0.35
        tax_amt = 15900000 + max_ratio * max_ratio
    elif std_assessment <= 300000000:
        txt_msg = '1억5천만원 초과, 3억원 이하 구간'
        max_ratio_amt, max_ratio = std_assessment - 150000000, 0.38
        tax_amt = 37600000 + max_ratio_amt * max_ratio
    elif std_assessment <= 500000000:
        txt_msg = '3억원 초과, 5억원 이하 구간'
        max_ratio_amt, max_ratio = std_assessment - 300000000, 0.4
        tax_amt = 94600000 + max_ratio_amt * max_ratio
    else:
        txt_msg = '5억원 초과 구간'
        max_ratio_amt, max_ratio = std_assessment - 500000000, 0.42
        tax_amt = 174600000 + max_ratio_amt * max_ratio
    acc_tax_ratio = tax_amt / std_assessment

    return int(tax_amt), acc_tax_ratio, txt_msg, max_ratio_amt, max_ratio


# input 신용/체크/현금영수증 이용금액(각각. 세금, 공과금, 통신비, 상품권구입, 신차구입, 해외사용은 제외한 금액)
# input 전통시장이용금액, 대중교통이용금액, 도서공연 이용금액
# input 총급여
# output : 신용/체크/현금영수증공제금액, 전통시장공제금액 ,대중교통공제금액, 도서공연공제금액, 신용카드공제대상금액, 체크/현금공제대상금액
def getCreditCrdEtcDeduction(credit_crd_use, debit_crd_use, cash_use, trad_market_use, public_trans_use, book_show_use,
                             total_salary):
    """
    :param credit_crd_use: 신용카드이용금액(세금, 공과금, 통신비, 상품권구입, 신차구입, 해외사용분은 제외)
    :param debit_crd_use:  체크카드이용금액(세금, 공과금, 통신비, 상품권구입, 신차구입, 해외사용분은 제외)
    :param cash_use: 현금영수증 이용금액(세금, 공과금, 통신비, 상품권구입, 신차구입, 해외사용분은 제외)
    :param trad_market_use: 전통시장 이용금액(위에랑 중복해도 괜찮음)
    :param public_trans_use: 대중교통 이용금액(위에랑 중복해도 괜찮음)
    :param book_show_use: 도서/공연 이용금액(위에랑 중복해도 괜찮음)
    :param total_salary: 총급여
    :return: 신용/체크/현금영수증 공제금액, 전통시장공제금액, 대중교통공제금액, 도서/공연공제금액
    :return:
    """
    total_use = credit_crd_use + debit_crd_use + cash_use
    hurdle = total_salary * 0.25

    book_show_deduction_limit = 0
    trad_market_deduction_limit = 1000000
    public_trans_deduction_limit = 1000000

    if total_salary <= 70000000:
        deduction_limit = min(3000000, total_salary*0.2)
        book_show_deduction_limit = 1000000
    elif total_salary <= 120000000:
        deduction_limit = 2500000
    else:
        deduction_limit = 2000000

    if total_use <= hurdle:
        return 0, 0, 0, 0, 0, 0, int(deduction_limit)
    else:
        if credit_crd_use > hurdle: # 신용카드만으로 공제문턱(총급여의 25%) 넘었을 때
            crd_etc_deduction = min((credit_crd_use - hurdle) * 0.15 + (debit_crd_use + cash_use) * 0.3,
                                    deduction_limit)
        else: # 세 개를 다 합쳤을 때 공제문턱(총급여의 25%)를 넘길 때
            crd_etc_deduction = min((total_use - hurdle) * 0.3, deduction_limit)
        # 신용카드의 공제 대상금액
        crd_card_deduce_valid_amt = max(credit_crd_use - hurdle, 0)
        # 체크/현금의 공제 대상금액
        deb_cash_deduce_valid_amt = debit_crd_use + cash_use

        trad_market_deduction = min(trad_market_use * 0.4, trad_market_deduction_limit)
        public_trans_deduction = min(public_trans_use * 0.4, public_trans_deduction_limit)
        book_show_deduction = min(book_show_use * 0.3, book_show_deduction_limit)

        return int(crd_etc_deduction), int(trad_market_deduction), int(public_trans_deduction), \
               int(book_show_deduction), int(crd_card_deduce_valid_amt), int(deb_cash_deduce_valid_amt), \
               int(deduction_limit)

def getHouseSaving(house_saving_amt, total_salary, householder_tf=0):
    """
    주택청약저축에 따른 소득공제금액 계산
    총급여 7천이하 & 무주택만 40% 공제, 공제한도 240만
    :param house_saving_amt:
    :return:
    """
    if total_salary > 70000000 or householder_tf ==1:
        return 0
    return min(int(house_saving_amt * 0.4), 2400000)

def getMyStock(my_stock):
    """
    우리사주 : 공제한도 400만원
    :param my_stock:
    :return:
    """
    return min(my_stock, 4000000)

def getBenefitPerUsage(userid, max_ratio, crd_card_use, deb_card_use, cash_use, total_salary,
                       deduction_limit, current_deduction_amt, unit_amt = 10000):
    """
    전년 신용카드 이용/청구내역 집계해서 신용카드 이용혜택율 계산(1만원당)
    max_ratio와 현재기준 신용/체크/현금 이용금액으로 절세혜택 계산 (1만원당) - 공제한도 감안해야
    :param userid:
    :param max_ratio:
    :return: 신용카드 절세금액(crd_tax_benefit), 현금/체크 절세금액(cash_deb_tax_benefit), 신용카드 혜택(crd_benefit),신용카드혜택비율
              신용카드혜택합계, 체크/현금 혜택합계,
    """
    # 전년도 신용카드 이용/청구내역 집계해서 신용카드 이용혜택율 계산
    # 전년도 청구상세내역 API 호출 & 가라데이터 만들어 붙이기 & 이용금액과 청구금액의 차이, 적립예정포인트율로 카드혜택크기 계산
    prev_y_df = shcSearchMonthlyBillingDetail('2018')
    input_aprvamt = int(prev_y_df['매출전표금액'][0])
    cardno = prev_y_df['이용카드뒷세자리'][0]
    prev_y_df = pd.concat([prev_y_df,genSHCBill(userid, input_aprvamt, cardno, '20180101', '20181231')])
    prev_y_df['적립예정포인트'] = prev_y_df['매출전표금액'] * prev_y_df['적립예정포인트율']
    prev_y_df['할인금액'] = prev_y_df['매출전표금액'] - prev_y_df['청구원금금액']
    crd_benefit_ratio = int(prev_y_df['적립예정포인트'].sum() + prev_y_df['할인금액'].sum()) / int(prev_y_df['매출전표금액'].sum())
    crd_benefit = unit_amt * crd_benefit_ratio

    # max_ratio와 현재기준 신용/체크/현금 이용금액으로 절세혜택 계산
    # 합계가 25%를 못넘은 경우
    huddle = total_salary * 0.25
    if crd_card_use + deb_card_use + cash_use < huddle:
        crd_tax_benefit = 0
        cash_deb_tax_benefit = 0
    # 합계는 25% 넘었는데.... 아예 현재 신용체크등등 공제금액이 공제한도를 초과한 경우
    elif deduction_limit <= current_deduction_amt:
        crd_tax_benefit = 0
        cash_deb_tax_benefit = 0
    # 합계는 25%를 넘었는데, 신용카드만으로는 25% 못넘은 경우
    elif crd_card_use < huddle:
        crd_tax_benefit = unit_amt * 0.3 * max_ratio
        cash_deb_tax_benefit = unit_amt * 0.3 * max_ratio
    # 신용카드만으로 25% 넘은 경우
    else:
        crd_tax_benefit = unit_amt * 0.15 * max_ratio
        cash_deb_tax_benefit = unit_amt * 0.3 * max_ratio

    return int(crd_tax_benefit), int(cash_deb_tax_benefit), int(crd_benefit), crd_benefit_ratio, \
           int(crd_tax_benefit+crd_benefit)

def getInsertComma(num):
    a = list(str(num))
    comma_position = []
    for i in range(len(a)):
        if divmod(i+1, 3)[1] == 1 and i+1 != 1:
            comma_position.append(-i)
    comma_position.reverse()
    for i in comma_position:
        a.insert(i, ',')
    return ''.join(a)
