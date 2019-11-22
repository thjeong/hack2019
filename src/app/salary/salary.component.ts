import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AlertService, AuthenticationService } from '@/_services';
import { User } from '@/_models';

@Component({
    selector: 'salary-cmp',
    templateUrl: 'salary.component.html'})
export class SalaryComponent implements OnInit {
    salaryForm: FormGroup;
    loading = false;
    submitted = false;
    returnUrl: string;
    currentUser: User;
    
    @Output() setStepInApp = new EventEmitter<number>();

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private alertService: AlertService
    ) {

        this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
        // redirect to home if already logged in
        if (this.authenticationService.currentUserValue) { 
            this.router.navigate(['/']);
        }
    }

    ngOnInit() {
        if (this.currentUser) { 
            this.salaryForm = this.formBuilder.group(this.currentUser);
        } else {
            this.salaryForm = this.formBuilder.group({
                total_salary: ['', Validators.required]
                //password: ['', Validators.required]
           });
        }

        // get return url from route parameters or default to '/'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    // convenience getter for easy access to form fields
    get f() { return this.salaryForm.controls; }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.salaryForm.invalid) {
            return;
        }

        this.loading = true;
        this.authenticationService.getSummary(this.currentUser) //, this.f.password.value)
            .pipe(first())
            .subscribe(
                data => {
                    console.log(data);
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