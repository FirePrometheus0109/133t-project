import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { InputLengths } from '../../../shared/constants/validators/input-length';
import { ValidationService } from '../../../shared/services/validation.service';
import { ResetUserPasswordActions } from '../../actions';
import { ResetUserPasswordState } from '../../states/reset-user-password.state';


@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password-page.component.html',
  styleUrls: ['./forgot-password-page.component.css']
})
export class ForgotPasswordPageComponent {
  @Select(ResetUserPasswordState.errors) errors$: Observable<any>;
  @Select(ResetUserPasswordState.temporaryEmail) temporaryEmail$: Observable<string>;

  forgotPasswordForm = new FormGroup({
    email: new FormControl('', Validators.compose(
      [Validators.required, Validators.maxLength(InputLengths.email), ValidationService.emailValidator]
    ))
  });

  constructor(private store: Store) {
  }

  sendLink(formValue: object) {
    this.store.dispatch(new ResetUserPasswordActions.SendForgotPassword(formValue));
  }
}
