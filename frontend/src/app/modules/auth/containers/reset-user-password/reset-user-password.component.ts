import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngxs/store';
import { UtilsService } from '../../../shared/services/utils.service';
import { ValidationService } from '../../../shared/services/validation.service';
import { ResetUserPasswordActions } from '../../actions';
import { RestoreCredentials, RestorePasswordCredentials } from '../../models/credentials.model';


@Component({
  selector: 'app-reset-user-password',
  templateUrl: './reset-user-password.component.html',
  styleUrls: ['./reset-user-password.component.css']
})
export class ResetUserPasswordComponent implements OnInit {
  public changePasswordForm = new FormGroup({
    passwords: new FormGroup({
      new_password: new FormControl('', Validators.compose([Validators.required, ValidationService.passwordValidator])),
      new_password_confirm: new FormControl('', Validators.compose([Validators.required, ValidationService.passwordValidator])),
    }, ValidationService.passwordMatchValidator),
  });

  private credentialData: RestoreCredentials;

  constructor(private store: Store,
              private route: ActivatedRoute) {
  }

  submitPassword(data) {
    this.isCredentialsExist ?
      this.store.dispatch(new ResetUserPasswordActions.ConfirmResetPassword(this.prepareConfirmData(data.passwords))) :
      this.store.dispatch(new ResetUserPasswordActions.SetPassword(data.passwords))
    ;
  }

  ngOnInit() {
    this.route.params.subscribe((params: RestoreCredentials) => {
      this.credentialData = params;
    });
  }

  public get isCredentialsExist() {
    return !UtilsService.isEmptyObject(this.credentialData);
  }

  private prepareConfirmData(passwords: RestorePasswordCredentials) {
    return Object.assign(passwords, this.credentialData);
  }
}
