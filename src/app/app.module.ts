import {HttpClientModule} from '@angular/common/http';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatNativeDateModule} from '@angular/material/core';
import {BrowserModule} from '@angular/platform-browser';
import {platformBrowserDynamic} from '@angular/platform-browser-dynamic';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import {MatExpansionModule} from '@angular/material/expansion';
import { MatInputModule } from '@angular/material';
import { MatButtonModule } from '@angular/material/button';
import {MatTableModule} from '@angular/material/table';

import {LoginComponent} from './login/login.component';
import { SalaryComponent } from './salary/salary.component';
import { SummaryComponent } from './summary/summary.component';
import { DetailComponent } from './detail/detail.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SalaryComponent,
    SummaryComponent,
    DetailComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    MatNativeDateModule,
    ReactiveFormsModule,
    MatExpansionModule,
    MatInputModule,
    MatButtonModule,
    MatTableModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
