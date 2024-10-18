import { Component, EventEmitter, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NavigationService } from '../../core/services/navigation.service';
import { BaseFormComponent } from '../../shared/components/base-form.component';
import { InputLengths } from '../../shared/constants/validators/input-length';
import { ValidationService } from '../../shared/services/validation.service';
import { SignupCredentials } from '../models/credentials.model';


@Component({
  selector: 'app-job-seeker-signup-form',
  template: `
    <mat-card>
      <mat-card-title>JobSeeker Signup</mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" ngxsForm="jssignup.form" ngxsFormClearOnDestroy="true" (ngSubmit)="submit()">

          <p>
            <mat-form-field>
              <input type="text" matInput placeholder="Email" formControlName="email">
            </mat-form-field>
            <app-control-messages [form]="form"
                                  [control]="f.email"
                                  [submitted]="isSubmitted"
                                  [errors]="errors">
            </app-control-messages>
          </p>

          <div formGroupName="passwords">
            <p>
              <mat-form-field>
                <input type="password" matInput placeholder="Password" formControlName="password1">
              </mat-form-field>
              <app-control-messages [form]="f.passwords"
                                    [control]="pf.password1"
                                    [submitted]="isSubmitted"
                                    [errors]="errors">
              </app-control-messages>
            </p>

            <p>
              <mat-form-field>
                <input type="password" matInput placeholder="Repeat Password" formControlName="password2">
              </mat-form-field>
              <app-control-messages [form]="f.passwords"
                                    [control]="pf.password2"
                                    [submitted]="isSubmitted"
                                    [errors]="errors">
              </app-control-messages>
            </p>

          </div>
          <app-control-messages [form]="f.passwords"
                                [control]="f.passwords"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>

          <p>
            <mat-form-field>
              <input type="text" matInput placeholder="First Name" formControlName="first_name">
            </mat-form-field>
            <app-control-messages [form]="form"
                                  [control]="f.first_name"
                                  [submitted]="isSubmitted"
                                  [errors]="errors">
            </app-control-messages>
          </p>

          <p>
            <mat-form-field>
              <input type="text" matInput placeholder="Last Name" formControlName="last_name">
            </mat-form-field>
            <app-control-messages [form]="form"
                                  [control]="f.last_name"
                                  [submitted]="isSubmitted"
                                  [errors]="errors">
            </app-control-messages>
          </p>

          <mat-button-toggle-group class="signupButtons">
            <button mat-raised-button color="warn" (click)="backToLogin()">Back to Login</button>
            <button type="submit" mat-raised-button color="primary" [disabled]="form.invalid">
              SignUp as JobSeeker
            </button>
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

    .signupButtons {
      display: flex;
      flex-direction: row;
      justify-content: flex-end;
    }
  `],
})
export class JobSeekerSignupComponent extends BaseFormComponent {
  @Output() submitted = new EventEmitter<SignupCredentials>();

  form: FormGroup = new FormGroup({
    email: new FormControl('',
      Validators.compose([Validators.required, ValidationService.emailValidator, Validators.maxLength(InputLengths.email)])),
    passwords: new FormGroup({
      password1: new FormControl('', Validators.compose([Validators.required, ValidationService.passwordValidator])),
      password2: new FormControl('', Validators.compose([Validators.required, ValidationService.passwordValidator])),
    }, ValidationService.passwordMatchValidator),
    first_name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
    last_name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
  });

  constructor(private navigationService: NavigationService) {
    super();
  }

  backToLogin() {
    this.navigationService.goToLoginPage();
  }
}
