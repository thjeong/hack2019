import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { User } from '@/_models';
import { Summary } from '@/_models';

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    private currentUserSubject: BehaviorSubject<User>;
    public currentUser: Observable<User>;

    private currentSummarySubject: BehaviorSubject<Summary>;
    public currentSummary: Observable<Summary>;
    private host_ip:string;

    constructor(private http: HttpClient) {
        this.currentUserSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
        this.currentUser = this.currentUserSubject.asObservable();

        this.currentSummarySubject = new BehaviorSubject<Summary>(JSON.parse(localStorage.getItem('currentSummary')));
        this.currentSummary = this.currentSummarySubject.asObservable();
        this.host_ip = window.location.origin;
    }

    public get currentUserValue(): User {
        return this.currentUserSubject.value;
    }

    public get currentSummaryValue(): Summary {
        return this.currentSummarySubject.value;
    }

    public updateSummaryValue(summary){
        this.currentSummarySubject.next(summary);
      }
    
    public setSummaryReqAddParms(n) {
        this.currentSummaryValue.req_add_trans = n;
    }

    login(userid: string) { //, password: string) {
        this.host_ip = window.location.origin;
        console.log('login to '+ this.host_ip);
        return this.http.post<any>(this.host_ip + '/login', { userid }) //, password })
            .pipe(map(user => {
                if (user) {
                    localStorage.setItem('currentUser', JSON.stringify(user));
                    this.currentUserSubject.next(user);
                    localStorage.removeItem('currentSummary');
                }

                return user;
            }));
    }

    getSummary(userid, total_salary) {
        this.host_ip = window.location.origin;
        console.log('getSummary for ' + userid + '(' + total_salary + ')' + ' to '+ this.host_ip);
        return this.http.post<any>(this.host_ip + '/summary', {'userid': userid, 'total_salary':total_salary})
            .pipe(map(summary => {
                if (summary) {
                    localStorage.setItem('currentSummary', JSON.stringify(summary));
                    this.currentSummarySubject.next(summary);
                }

                return summary;
            }));
    }

    getDetail(summaryinfo: Summary) {
        this.host_ip = window.location.origin;
        console.log('getDetail for ' + summaryinfo + ' to '+ this.host_ip);
        return this.http.post<any>(this.host_ip + '/detail', summaryinfo)
            .pipe(map(summary => {
                if (summary) {
                    localStorage.setItem('currentSummary', JSON.stringify(summary));
                    this.currentSummarySubject.next(summary);
                }

                return summary;
            }));
    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
        localStorage.removeItem('currentSummary');
        this.currentUserSubject.next(null);
        this.currentSummarySubject.next(null);
    }
}