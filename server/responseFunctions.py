import json
from server.genDummyData import genSHBAccountTrans
from server.taxFunctions import simple_tax_calc
# from genDummyData import genSHBAccountTrans
# from taxFunctions import simple_tax_calc

def login_func(userid, year='2018'):
    """
    user id 받아서 전년도 급여내역 정리해서 알려주기
    :param userid:
    :return:
    """
    # api 호출 & dataframe으로 parsing하는 모듈 추가
    shb_trans_df = genSHBAccountTrans(userid)
    net_income = shb_trans_df[shb_trans_df['적요'].str.contains('급여')]['입금'].sum()
    total_salary = simple_tax_calc(net_income, 'server/data/')
    output_json = json.dumps({'userid' : userid, 'total_salary': total_salary})
    return output_json