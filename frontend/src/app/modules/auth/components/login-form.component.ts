import { Component, EventEmitter, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NavigationService } from '../../core/services/navigation.service';
import { BaseFormComponent } from '../../shared/components/base-form.component';
import { ValidationService } from '../../shared/services/validation.service';
import { Credentials } from '../models/credentials.model';


@Component({
  selector: 'app-login-form',
  template: `
    <mat-card>
      <mat-card-title>Login</mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" ngxsForm="login.form" ngxsFormClearOnDestroy="true" (ngSubmit)="submit()">
          <p>
            <mat-form-field>
              <input type="text" matInput placeholder="Email" formControlName="email">
            </mat-form-field>
            <app-control-messages [form]="form"
                                  [control]="f.email"
                                  [submitted]="isSubmitted">
            </app-control-messages>
          </p>

          <p>
            <mat-form-field>
              <input type="password" matInput placeholder="Password" formControlName="password">
            </mat-form-field>
            <app-control-messages [form]="form"
                                  [control]="f.password"
                                  [submitted]="isSubmitted">
            </app-control-messages>
          </p>

          <p>
            <span class="link" (click)="goToForgotPassword()">Forgot your password?</span>
          </p>

          <mat-button-toggle-group class="loginButtons">
            <button type="submit" mat-raised-button color="primary">Login</button>
          </mat-button-toggle-group>

          <mat-divider [inset]="true"></mat-divider>
          <app-social-auth></app-social-auth>
          <mat-divider [inset]="true"></mat-divider>

          <mat-button-toggle-group class="loginButtons">
            <button mat-raised-button routerLink="." (click)="goToCompanySignup()">Company Signup</button>
            <button mat-raised-button routerLink="." (click)="goToJobSeekerSignup()">JobSeeker Signup</button>
          </mat-button-toggle-group>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    :host {
      display: flex;
      justify-content: center;
      margin: 72px 0;
    }

    .mat-form-field {
      width: 100%;
      min-width: 300px;
    }

    mat-card-title,
    mat-card-content {
      display: flex;
      justify-content: center;
    }

    .loginButtons {
      display: flex;
      flex-direction: row;
      justify-content: flex-end;
    }

    mat-divider {
      margin-top: 20px !important;
      margin-bottom: 20px !important;
    }
  `],
})
export class LoginFormComponent extends BaseFormComponent {
  @Output() submitted = new EventEmitter<Credentials>();
  @Output() forgotPassword = new EventEmitter<string>();

  form: FormGroup = new FormGroup({
    email: new FormControl('', Validators.compose([Validators.required, ValidationService.emailValidator])),
    password: new FormControl('', Validators.required),
  });

  constructor(private navigationService: NavigationService) {
    super();
  }

  goToJobSeekerSignup() {
    this.navigationService.goToJobSeekerSignUpPage();
  }

  goToCompanySignup() {
    this.navigationService.goToCompanySignUpPage();
  }

  goToForgotPassword() {
    this.forgotPassword.emit(this.form.value.email);
  }
}
