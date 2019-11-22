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

@Component({
    selector: 'detail-cmp',
    templateUrl: 'detail.component.html'})
export class DetailComponent implements OnInit {
    loading = false;
    returnUrl: string;
    benefitPer10kColumns: string[] = ['type', 'credit', 'debit'];
    cardTransactionColumns: string[] = ['position', 'name', 'weight', 'symbol'];
    benefitSource: BenefitElement[]
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
        
        this.benefitSource = [
            // {type: '신용', tax: this.currentSummary.crd_tax_benefit, card: this.currentSummary.crd_benefit + ' (' + (Math.round(this.currentSummary.crd_benefit_ratio * 1000) / 100).toString() + ' %)', total:this.currentSummary.crd_benefit_sum},
            // {type: '체크', tax: this.currentSummary.deb_cash_tax_benefit, card: '', total:this.currentSummary.deb_cash_tax_benefit}
            {type: '세금', credit: this.currentSummary.crd_tax_benefit.toString(), debit:  this.currentSummary.deb_cash_tax_benefit},
            {type: '카드', credit: this.currentSummary.crd_benefit + ' (' + (Math.round(this.currentSummary.crd_benefit_ratio * 1000) / 100).toString() + ' %)', debit: 0}
        ];
        console.log('summary to table', this.benefitSource.toString());
    }
}