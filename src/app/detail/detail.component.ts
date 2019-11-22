import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { Summary } from '@/_models/summary';
import { AlertService, AuthenticationService } from '@/_services';

export interface BenefitElement {
    type: string;
    credit: string;
    debit: number;
  }

export interface TransactionElement {
    apv_d: string;
    crd_tcd: string;
    apv_amt: number;
    mct_nm: string;
    benefit: number;
}
  
@Component({
    selector: 'detail-cmp',
    templateUrl: 'detail.component.html',
    styleUrls: ['./detail.component.css']})
export class DetailComponent implements OnInit {
    loading = false;
    returnUrl: string;
    benefitPer10kColumns: string[] = ['type', 'credit', 'debit'];
    cardTransactionColumns: string[] = ['apv_d', 'crd_tcd', 'apv_amt', 'mct_nm', 'benefit'];
    benefitSource: BenefitElement[]
    transactionSource: TransactionElement[]
    currentSummary:Summary;

    @Output() setStepInApp = new EventEmitter<number>();

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private alertService: AlertService
    ) {
        this.authenticationService.currentSummary.subscribe(x => this.currentSummary = x);
    }

    ngOnInit() {
        this.benefitSource = this.getBenefitSource();
        this.transactionSource = this.currentSummary.recent_crd_deb_use_list;
        console.log('benefitSource', this.benefitSource.toString());
        console.log('transactionSource', this.transactionSource.toString());
    }

    // refreshValues() {
    //     this.benefitSource = this.getBenefitSource();
    //     this.transactionSource = this.currentSummary.recent_crd_deb_use_list;
    // }

    getBenefitSource() {
        return [
            {type: '절세금액', credit: '' + this.currentSummary.crd_tax_benefit, debit:  this.currentSummary.deb_cash_tax_benefit},
            {type: '카드혜택', credit: this.currentSummary.crd_benefit + ' (' + (Math.round(this.currentSummary.crd_benefit_ratio * 1000) / 100).toString() + ' %)', debit: 0}
        ];
    }
}