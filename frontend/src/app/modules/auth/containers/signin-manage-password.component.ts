import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { ValidationService } from '../../shared/services/validation.service';
import { SigninManagePasswordActions } from '../actions';
import { RestoreCredentials } from '../models/credentials.model';
import { AuthState } from '../states/auth.state';
import { SigninManagePasswordState } from '../states/signin-manage-password.state';


@Component({
  selector: 'app-signin-manage-password',
  template: `
    <mat-card>
      <mat-card-title align="center">
        <span *ngIf="!(invitationMode$ | async)">Restore confirmation</span>
        <span *ngIf="invitationMode$ | async">Enter password</span>
      </mat-card-title>
      <mat-card-subtitle align="center" *ngIf="!(invitationMode$ | async)">
        Please confirm restore your account
      </mat-card-subtitle>
      <mat-card-content>
        <app-change-password-form [form]="changePasswordForm"
                                  (submitted)="submitPassword($event)">
        </app-change-password-form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class SigninManagePasswordComponent implements OnInit {
  @Select(SigninManagePasswordState.invitationMode) invitationMode$: Observable<boolean>;

  constructor(private store: Store,
              private navigationService: NavigationService,
              private route: ActivatedRoute) {
  }

  public changePasswordForm = new FormGroup({
    passwords: new FormGroup({
      new_password: new FormControl('', Validators.compose([Validators.required, ValidationService.passwordValidator])),
      new_password_confirm: new FormControl('', Validators.compose([Validators.required, ValidationService.passwordValidator])),
    }, ValidationService.passwordMatchValidator),
  });

  ngOnInit() {
    if (this.store.selectSnapshot(AuthState.isAuthorized)
      && this.store.selectSnapshot(SigninManagePasswordState.invitationMode)) {
      this.navigationService.goToHomePage();
      this.showAlreadyLoggedInNotification();
    }
    this.route.params.subscribe((params: RestoreCredentials) => {
      this.store.dispatch(new SigninManagePasswordActions.SetParams(params));
    });
  }

  public submitPassword(passwordData) {
    const restoreData = {
      new_password: passwordData.passwords.new_password,
      token: this.store.selectSnapshot(SigninManagePasswordState.token),
      user: this.store.selectSnapshot(SigninManagePasswordState.user)
    };
    if (this.store.selectSnapshot(SigninManagePasswordState.invitationMode)) {
      this.store.dispatch(new SigninManagePasswordActions
        .SetPasswordForInvitedUser(Object.assign(restoreData, {new_password_confirm: passwordData.passwords.new_password_confirm})));
    } else {
      this.store.dispatch(new SigninManagePasswordActions.RestoreAccount(restoreData));
    }
  }

  private showAlreadyLoggedInNotification() {
    const message = 'You are already logged in!';
    this.store.dispatch(new CoreActions.SnackbarOpen({
      message,
      type: SnackBarMessageType.DEFAULT_MESSAGE_TYPE,
    }));
  }
}
