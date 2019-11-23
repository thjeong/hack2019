import { Component, Output, Input, EventEmitter, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { interval } from 'rxjs';

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
    //benefitSource: BenefitElement[]
    // transactionSource: TransactionElement[]
    currentSummary:Summary;
    progressBar: number[] = [0,500,0,500];
    div1: number;
    div2: number;


    @Input() benefitSource = [
        // {type: '절세금액', credit: '' + this.currentSummary.crd_tax_benefit, debit:  this.currentSummary.deb_cash_tax_benefit},
        // {type: '카드혜택', credit: this.currentSummary.crd_benefit + ' (' + (Math.round(this.currentSummary.crd_benefit_ratio * 1000) / 100).toString() + ' %)', debit: 0}
    ];
    @Input() transactionSource = [];

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
        const animationCounter = interval(50);
        animationCounter.subscribe(this.animateBar());
        //this.benefitSource = this.getBenefitSource();
        // this.transactionSource = this.currentSummary.recent_crd_deb_use_list;
        // console.log('benefitSource', this.benefitSource.toString());
        // console.log('transactionSource', this.transactionSource.toString());

    }

    animateBar() {
        return (function(self) {
            return function() {
                if (self.currentSummary) {
                    self.div1 = Math.round(Math.min(self.currentSummary.crd_etc_use_amt / self.currentSummary.crd_etc_deduce_hurdle, 1) * 50);
                    self.div2 = Math.round(Math.min(self.currentSummary.crd_etc_deduce / self.currentSummary.crd_etc_deduction_limit, 1) * 50);

                    //console.log('divs, progressbars', [self.div1, self.div2], self.progressBar);
                    
                    if (self.progressBar[2] > 0) {
                        if (self.div2 > self.progressBar[2]) {
                            self.progressBar[2] += 1;
                        } else if (self.div2 < self.progressBar[2]) {
                            self.progressBar[2] -= 1;
                        }
                    } else if (self.progressBar[2] == 0) {
                        if (self.div1 > self.progressBar[0]) {
                            self.progressBar[0] += 1;
                        } else if (self.div1 < self.progressBar[0]) {
                            self.progressBar[0] -= 1;
                        } else if (self.div2 > self.progressBar[2]) {
                            self.progressBar[2] += 1;
                        }
                    }

                    self.progressBar[1] = 50 - self.progressBar[0];
                    self.progressBar[3] = 50 - self.progressBar[2];
                }
            }
        })(this);
    }

    refreshValues() {
        // this.benefitSource = this.getBenefitSource();
        // this.transactionSource = this.currentSummary.recent_crd_deb_use_list;
        console.log('right here!');
    }

    
}