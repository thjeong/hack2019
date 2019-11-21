import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthenticationService } from './_services';
import { User } from './_models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  step = 0;
  currentUser: User;

  constructor(
      private router: Router,
      private authenticationService: AuthenticationService
  ) {
      this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
      if (this.authenticationService.currentUserValue) {
        // 로그인 된 유저가 있는 경우는 일단 1번째 페이지로? (2번째 페이지로 가야할 듯?)
        this.setStep(1);
      }
  }

  setStep(index: number) {
    this.step = index;
  }

  logout() {
      this.authenticationService.logout();
      this.router.navigate(['/login']);
  }
}
