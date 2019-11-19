# 세후 급여액으로 (세전)총급여액 계산 망했음.
def _simple_tax_calc(n_of_members, net_income, table_file_dir = './'):
    import scipy.interpolate as spi
    import numpy as np
    import pandas as pd
    import json
    import os
    with open(os.path.join(table_file_dir, 'max_tax.json')) as f:
        max_tax = json.load(f)  # 공제대상가족 인원수별 세후 1억원 급여자의 월세액
    df = pd.read_csv(os.path.join(table_file_dir, 'tax_table.tsv'), sep='\t')
    # net income이 일정금액(세전월급여 1억원 이상에 해당하는 금액) 이상이면 별도 테이블 참조
    over120M_pt = df.tail(1)[str(n_of_members)].iloc[0]  # 세전 월 1억(연12억) 이상의 실수령액
    if net_income > over120M_pt:
        tmp_total_salary = (net_income + max_tax[str(n_of_members)] * 12 - 10000000 * 12 * 0.98 * 0.35) / (
        1 - 0.98 * 0.35)
        if tmp_total_salary / 12 > 14000000:
            tmp_total_salary = (
                               net_income + max_tax[str(n_of_members)] * 12 + 1372000 - 14000000 * 12 * 0.98 * 0.38) / (
                               1 - 0.98 * 0.38)
        elif tmp_total_salary / 12 > 28000000:
            tmp_total_salary = (net_income + max_tax[str(n_of_members)] * 12 + 6585600 - 28000000 * 12 * 0.98 * 0.4) / (
            1 - 0.98 * 0.4)
        elif tmp_total_salary / 12 > 45000000:
            tmp_total_salary = (net_income + max_tax[
                str(n_of_members)] * 12 + 13249600 - 45000000 * 12 * 0.98 * 0.42) / (1 - 0.98 * 0.42)
        return tmp_total_salary
    x = np.array(df[str(n_of_members)])
    y = np.array(df['total_income'])
    split_idx = np.where(y == 70080000)[0][0]
    if net_income >= x[split_idx]:
        x = x[split_idx:]
        y = y[split_idx:]
    else:
        x = x[:split_idx]
        y = y[:split_idx]
    ipo = spi.splrep(x, y, k=1)
    return spi.splev(net_income, ipo).max()


# 총 급여액으로 근로소득공제금액 계산
def getEarnedIncomeDeduction(total_salary):
    """
    총 급여액으로 근로소득공제금액 계산
    :param total_salary: 총 급여(세전)
    :return: 근로소득공제금액
    """
    if total_salary <= 5000000: # 500만원 이하. 급여액의 70%
        return total_salary * 0.7
    elif total_salary <= 15000000: # 500만원초과, 1500만원 이하
        return 3500000 + (total_salary - 5000000) * 0.4
    elif total_salary <= 45000000: # 1500만원 초과, 4500만원 이하
        return 7500000 + (total_salary - 15000000) * 0.15
    elif total_salary <= 100000000: # 4500만원 초과, 1억 이하
        return 12000000 + (total_salary - 45000000) * 0.05
    else: # 1억원 초과
        return 14750000 + (total_salary - 100000000) * 0.02

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
    return total_salary * 0.045

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
            return 3100000 + total_salary * 0.04
        elif n_of_members == 2:
            return 3600000 + total_salary * 0.04
        else:
            return 5000000 + total_salary * 0.07 + max(total_salary - 40000000, 0) * 0.04
    elif total_salary <= 45000000:
        if n_of_members == 1:
            return 3100000 + total_salary * 0.04 - (total_salary - 30000000) * 0.05
        elif n_of_members == 2:
            return 3600000 + total_salary * 0.04 - (total_salary - 30000000) * 0.05
        else:
            return 5000000 + total_salary * 0.07 - (total_salary - 30000000) * 0.05 \
                   + max(total_salary - 40000000, 0) * 0.04
    elif total_salary <= 70000000:
        if n_of_members == 1:
            return 3100000 + total_salary * 0.015
        elif n_of_members == 2:
            return 3600000 + total_salary * 0.02
        else:
            return 5000000 + total_salary * 0.05 + (total_salary - 40000000) * 0.04
    else:
        if n_of_members == 1:
            return 3100000 + total_salary * 0.005
        elif n_of_members == 2:
            return 3600000 + total_salary * 0.01
        else:
            return 5000000 + total_salary * 0.03 + (total_salary - 40000000) * 0.04


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

    return tax_amt, acc_tax_ratio, txt_msg, max_ratio_amt, max_ratio


# input 신용/체크/현금영수증 이용금액(각각. 세금, 공과금, 통신비, 상품권구입, 신차구입, 해외사용은 제외한 금액)
# input 전통시장이용금액, 대중교통이용금액, 도서공연 이용금액
# input 총급여
# output : 신용/체크/현금영수증공제금액, 전통시장공제금액 ,대중교통공제금액, 도서공연공제금액
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
    deduction_min_use = total_salary * 0.25

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

    if total_use <= deduction_min_use:
        return 0, 0, 0, 0
    else:
        if credit_crd_use > deduction_min_use: # 신용카드만으로 공제문턱(총급여의 25%) 넘었을 때
            crd_etc_deduction = min((credit_crd_use - deduction_min_use) * 0.15 + (debit_crd_use + cash_use) * 0.3,
                                    deduction_limit)
        else:
            crd_etc_deduction = min((total_use - deduction_min_use) * 0.3, deduction_limit)

        trad_market_deduction = min(trad_market_use * 0.4, trad_market_deduction_limit)
        public_trans_deduction = min(public_trans_use * 0.4, public_trans_deduction_limit)
        book_show_deduction = min(book_show_use * 0.3, book_show_deduction_limit)

        return crd_etc_deduction, trad_market_deduction, public_trans_deduction, book_show_deduction
