import { Component, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import { AuthenticationService } from './_services';
import { User } from './_models';
import { Summary } from './_models';

// import { DetailComponent } from './detail';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  step = 0;
  currentUser: User;
  currentSummary: Summary;

  constructor(
      private router: Router,
      private authenticationService: AuthenticationService
  ) {
      this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
      this.authenticationService.currentSummary.subscribe(x => this.currentSummary = x);
      if (this.authenticationService.currentUserValue) {
        // 로그인 된 유저가 있는 경우는 일단 1번째 페이지로? (2번째 페이지로 가야할 듯?)
        this.setStep(1);
      }
  }
  // @ViewChild(DetailComponent, {static: false}) private detailComp: DetailComponent;

  setStep(index: number) {
    this.step = index;
    // this.detailComp.refreshValues();
  }

  getBenefitSource() {
    if (this.currentSummary) {
        return [
          {type: '절세금액', credit: '' + this.currentSummary.crd_tax_benefit, debit:  this.currentSummary.deb_cash_tax_benefit},
          {type: '카드혜택', credit: this.currentSummary.crd_benefit + ' (' + (Math.round(this.currentSummary.crd_benefit_ratio * 1000) / 100).toString() + ' %)', debit: 0}
      ];
    }
  }

  logout() {
      this.authenticationService.logout();
      this.router.navigate(['/login']);
  }
}
