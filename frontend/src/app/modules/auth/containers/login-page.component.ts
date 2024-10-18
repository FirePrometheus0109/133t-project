import { Component } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../core/services/navigation.service';
import { LoginPageActions, ResetUserPasswordActions } from '../actions';
import { Credentials } from '../models/credentials.model';
import { LoginFormState } from '../states/login-page.state';


@Component({
  selector: 'app-login-page',
  template: `
    <app-login-form (submitted)="onSubmit($event)"
                    (forgotPassword)="forgotPassword($event)"
                    [pending]="pending$ | async"
                    [errors]="errors$ | async">
    </app-login-form>
  `,
  styles: [],
})
export class LoginPageComponent {
  @Select(LoginFormState.pending) pending$: Observable<boolean>;
  @Select(LoginFormState.errors) errors$: Observable<any>;

  constructor(private store: Store,
              private navigationService: NavigationService) {
  }

  onSubmit(credentials: Credentials) {
    this.store.dispatch(new LoginPageActions.Login(credentials));
  }

  forgotPassword(email: string) {
    this.store.dispatch(new ResetUserPasswordActions.SetTemporaryEmailField(email));
    this.navigationService.goToForgotPasswordPage();
  }
}
