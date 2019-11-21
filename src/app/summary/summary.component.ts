import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AlertService, AuthenticationService } from '@/_services';

@Component({
    selector: 'summary-cmp',
    templateUrl: 'summary.component.html'})
export class SummaryComponent implements OnInit {
    summaryForm: FormGroup;
    loading = false;
    submitted = false;
    returnUrl: string;
    
    @Output() setStepInApp = new EventEmitter<number>();

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private alertService: AlertService
    ) {
        // redirect to home if already logged in
        if (this.authenticationService.currentUserValue) { 
            this.router.navigate(['/']);
        }
    }

    ngOnInit() {
        this.summaryForm = this.formBuilder.group({
            earned_income_deduce: ['', Validators.required],
            personal_allowance: ['', Validators.required],
            pension_insurance_deduce: ['', Validators.required]
            //password: ['', Validators.required]
        });

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
        this.authenticationService.getSummary(this.authenticationService.currentUserValue) //, this.f.password.value)
            .pipe(first())
            .subscribe(
                data => {
                    this.loading = false;
                    this.setStepInApp.emit(2);
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