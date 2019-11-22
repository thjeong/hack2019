export class Summary {
    earned_income_deduce : number; //소득공제금액
    personal_allowance_deduce : number; //인적공제금액
    pension_insurance_deduce : number; //연금보험료공제금액
    spec_income_deduce : number; //특별소득공제금액
    crd_card_use : number; //신용카드이용금액
    deb_card_use : number; //체크카드이용금액
    cash_use : number; //현금영수증이용금액
    crd_etc_use_amt : number; //신용체크현금 이용금액합계
    crd_etc_deduce : number; //신용체크현금영수증 소득공제금액
    crd_etc_deduce_hurdle : number; //신용체크현금영수증 소득공제 허들
    public_trans_use : number; //대중교통 이용금액
    public_trans_deduce : number; //대중교통 소득공제금액
    trad_market_use : number; //전통시장 이용금액
    trad_market_deduce : number; //전통시장 소득공제금액
    book_use : number; //도서/공연 이용금액
    book_deduce : number; //도서/공연 소득공제금액
    house_saving : number; //주택청약저축금액
    house_saving_deduce : number; //주택청약저축 공제금액
    my_stock : number; //우리사주조합출연금
    my_stock_deduce : number; //우리사주조합출연금 공제금액
    etc_deduce : number; //기타 공제금액
    total_deduce : number; //공제금액합계
    householder_tf : number; //유주택TF
    n_of_members : number; //인적공제대상 인원

    std_assessment : number; //과세표준금액
    tax_amt : number; //산출세액
    acc_tax_ratio : number; //누적세율
    txt_msg: string; //적용구간(텍스트)
    max_ratio : number; //현재적용세율(최대세율)
    huddle_remains : number; //신용/체크/현금 소득공제 문턱 잔여금액

    crd_tax_benefit : number; //신용카드 절세금액(1만원당)
    deb_cash_tax_benefit : number; //체크/현금 절세금액(1만원당)
    crd_benefit : number; //신용카드 혜택금액(1만원당)
    crd_benefit_ratio : number; //신용카드 혜택율
    crd_benefit_sum : number; //신용카드 혜택합계(1만원당 절세금액 + 카드혜택)

    public_trans_deduce_limit : number; //대중교통 공제한도
    public_trans_benefit : number; //대중교통 절세금액(1만원당)
    trad_markeet_deduce_limit : number; //전통시장 공제한도
    trad_market_benefit : number; //전통시장 절세금액(1만원당)
}