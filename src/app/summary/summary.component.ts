import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AlertService, AuthenticationService } from '@/_services';

import { Summary } from '@/_models';

@Component({
    selector: 'summary-cmp',
    templateUrl: 'summary.component.html'})
export class SummaryComponent implements OnInit {
    summaryForm: FormGroup;
    loading = false;
    submitted = false;
    returnUrl: string;
    currentSummary: Summary;

    summary_values = [
        {'key': 'spec_income_deduce', 'title': '특별공제금액'}
    ]
    
    @Output() setStepInApp = new EventEmitter<number>();

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private alertService: AlertService
    ) {
        this.authenticationService.currentSummary.subscribe(x => this.currentSummary = x);
    }

    ngOnInit() {
        // this.summaryForm = this.formBuilder.group({
        //     earned_income_deduce: ['', Validators.required],
        //     personal_allowance: ['', Validators.required],
        //     pension_insurance_deduce: ['', Validators.required]
        // });

        // if(this.currentSummary) {
            this.summaryForm = this.formBuilder.group(this.currentSummary);
        // } else {
        //     this.summaryForm = this.formBuilder.group({
        //             earned_income_deduce: ['', Validators.required],
        //             personal_allowance: ['', Validators.required],
        //             pension_insurance_deduce: ['', Validators.required],
        //             spec_income_deduce: ['', Validators.required],
        //             crd_card_use: ['', Validators.required],
        //             deb_card_use: ['', Validators.required],
        //             cash_use: ['', Validators.required],
        //             public_trans_use: ['', Validators.required],
        //             trad_market_use: ['', Validators.required],
        //             book_use: ['', Validators.required],
        //             house_saving: ['', Validators.required],
        //             my_stock: ['', Validators.required],
        //             etc_deduce: ['', Validators.required]
        //         });
        // }
        

        // get return url from route parameters or default to '/'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    // convenience getter for easy access to form fields
    get f() { return this.summaryForm.controls; }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.summaryForm.invalid) {
            return;
        }

        
        this.loading = true;
        //console.log('formGroup', this.summaryForm.value);
        this.authenticationService.getDetail(this.summaryForm.value) // this.currentSummary)
            .pipe(first())
            .subscribe(
                data => {
                    console.log(data);
                    this.loading = false;
                    this.setStepInApp.emit(3);
                    //this.router.navigate([this.returnUrl]);
                },
                error => {
                    this.alertService.error(error);
                    this.loading = false;
                });
    }

    logout() {
        this.authenticationService.logout();
//        this.router.navigate(['/login']);
    }
}