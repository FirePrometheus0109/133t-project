import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { BaseFormComponent } from '../../shared/components/base-form.component';
import { InputLengths } from '../../shared/constants/validators/input-length';
import { ValidationService } from '../../shared/services/validation.service';
import { UpdatePasswordCredentials } from '../models/credentials.model';
import { AccountPageState } from '../states/account-page.state';


@Component({
  selector: 'app-edit-account-password-form',
  template: `
    <mat-card>
      <form [formGroup]="form" (ngSubmit)="submit()">
        <mat-card-content>
          <mat-form-field>
            <input matInput formControlName="old_password" placeholder="Old password" required
                   [type]="hideOldPassword ? 'password' : 'text'">
            <mat-icon matSuffix (click)="hideOldPassword = !hideOldPassword">
              {{hideOldPassword ? 'visibility_off' : 'visibility'}}
            </mat-icon>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.old_password"
                                [submitted]="isSubmitted">
          </app-control-messages>
        </mat-card-content>

        <mat-card-content>
          <mat-form-field>
            <input matInput formControlName="new_password" placeholder="New password" required
                   [type]="hideNewPassword ? 'password' : 'text'">
            <mat-icon matSuffix (click)="hideNewPassword = !hideNewPassword">
              {{hideNewPassword ? 'visibility_off' : 'visibility'}}
            </mat-icon>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.new_password"
                                [submitted]="isSubmitted">
          </app-control-messages>
          <!-- TODO: temporary solution. Needs work with app-control-messages for server errors -->
          <span *ngIf="(errors$ | async)?.errors?.old_password" class="style-error">
            {{(errors$ | async)?.errors?.old_password.join()}}
          </span>
        </mat-card-content>
        <div class="controls-container">
          <button type="submit" mat-button color="primary">Update password</button>
          <button mat-button color="primary" (click)="dialogRef.close()">Cancel</button>
        </div>
      </form>
    </mat-card>
  `,
  styles: [`
    mat-form-field {
      width: 100%;
    }
  `],
})
export class EditAccountPasswordFormComponent extends BaseFormComponent {
  @Select(AccountPageState.errors) errors$: Observable<any>;

  @Output() submitted = new EventEmitter<UpdatePasswordCredentials>();

  public form: FormGroup = new FormGroup({
    old_password: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.password)])),
    new_password: new FormControl('', Validators.compose([ValidationService.passwordValidator, Validators.maxLength(InputLengths.password),
       Validators.required])),
  });

  public hideOldPassword = true;
  public hideNewPassword = true;

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>) {
    super();
  }
}
