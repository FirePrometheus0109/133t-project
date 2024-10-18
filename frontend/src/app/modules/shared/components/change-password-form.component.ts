import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { BaseFormComponent } from '../../shared/components/base-form.component';


@Component({
  selector: 'app-change-password-form',
  template: `
    <mat-card>
      <form [formGroup]="form" (ngSubmit)="submit()">
        <mat-card-content *ngIf="form.controls.old_password">
          <mat-form-field>
            <input matInput formControlName="old_password" placeholder="Old password" required
                   [type]="hideOldPassword ? 'password' : 'text'">
            <mat-icon matSuffix (click)="hideOldPassword = !hideOldPassword">
              {{hideOldPassword ? 'visibility_off' : 'visibility'}}
            </mat-icon>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.old_password"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
        </mat-card-content>

        <mat-card-content formGroupName="passwords">
          <mat-form-field>
            <input matInput formControlName="new_password" placeholder="New password" required
                   [type]="hideNewPassword ? 'password' : 'text'">
            <mat-icon matSuffix (click)="hideNewPassword = !hideNewPassword">
              {{hideNewPassword ? 'visibility_off' : 'visibility'}}
            </mat-icon>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="passwordControls.new_password"
                                [submitted]="isSubmitted">
          </app-control-messages>
          <mat-form-field>
            <input matInput formControlName="new_password_confirm" placeholder="Confirm password" required
                   [type]="hideConfirmPassword ? 'password' : 'text'">
            <mat-icon matSuffix (click)="hideConfirmPassword = !hideConfirmPassword">
              {{hideConfirmPassword ? 'visibility_off' : 'visibility'}}
            </mat-icon>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="passwordControls.new_password_confirm"
                                [submitted]="isSubmitted">
          </app-control-messages>

          <app-control-messages [form]="form"
                                [control]="f.passwords"
                                [submitted]="isSubmitted">
          </app-control-messages>
        </mat-card-content>
        <div class="controls-container">
          <button type="submit" mat-raised-button color="primary" [disabled]="form.invalid">
            <span *ngIf="checkIsModal()">Update password</span>
            <span *ngIf="!checkIsModal()">Confirm</span>
          </button>
          <button *ngIf="checkIsModal()" mat-button color="primary" (click)="dialogRef.close()">Cancel</button>
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
export class ChangePasswordFormComponent extends BaseFormComponent {
  public hideOldPassword = true;
  public hideNewPassword = true;
  public hideConfirmPassword = true;

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>) {
    super();
  }

  public get passwordControls() {
    return this.form.controls.passwords['controls'];
  }

  checkIsModal() {
    return this.modalData.length > 0;
  }
}
