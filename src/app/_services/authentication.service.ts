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

    login(userid: string) { //, password: string) {
        console.log('login to '+ this.host_ip);
        return this.http.post<any>(this.host_ip + '/login', { userid }) //, password })
            .pipe(map(user => {
                if (user) {
                    localStorage.setItem('currentUser', JSON.stringify(user));
                    this.currentUserSubject.next(user);
                }

                return user;
            }));
    }

    getSummary(userinfo: User) {
        console.log('getSummary for ' + userinfo);
        return this.http.post<any>(this.host_ip + '/summary', userinfo)
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
        this.currentUserSubject.next(null);
    }
}