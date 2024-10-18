import { Component, EventEmitter, Inject, Output } from '@angular/core';
import { FormControl, FormGroup, ValidatorFn, Validators } from '@angular/forms';
import { MatRadioChange } from '@angular/material';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { environment } from '../../../../environments/environment';
import { InputLengths } from '../constants/validators/input-length';


@Component({
  selector: 'app-delete-account-dialog',
  template: `
    <h3 mat-dialog-title align="center">Account Deletion</h3>
    <h4 mat-dialog-title align="center">We are upset that you decided to stop working with 133T.</h4>
    <mat-dialog-content align="center">
      <form [formGroup]="deletionForm">
        <mat-radio-group formControlName="text" class="variants" (change)="onReasonChange($event)">
          <span>It is very important to us to know the reason of deletion account. Please provide the reason:</span>
          <div *ngFor="let deletionVariant of data.account_deletion_reasons">
            <mat-radio-button [value]="deletionVariant">
              {{deletionVariant}}
            </mat-radio-button>
            <mat-form-field *ngIf="showTextAreaReason(deletionVariant)" class="example-full-width">
              <textarea matInput placeholder="Type your reason" formControlName="other"></textarea>
            </mat-form-field>
          </div>
        </mat-radio-group>
      </form>
    </mat-dialog-content>
    <mat-dialog-actions align="center">
      <button mat-raised-button color="primary" (click)="deleteWithReason(deletionForm)"
              [disabled]="deletionForm.invalid">
        <mat-icon matSuffix>check</mat-icon>
        Delete
      </button>
      <button type="button" mat-raised-button matDialogClose color="primary">
        <span>Close</span>
        <mat-icon matSuffix>close</mat-icon>
      </button>
    </mat-dialog-actions>
  `,
  styles: [`
    .variants {
      display: flex;
      flex-direction: column;
    }
  `]
})
export class DeleteAccountDialogComponent {
  @Output() confirmed = new EventEmitter<any>();

  deletionForm = new FormGroup({
    text: new FormControl('', Validators.required),
    other: new FormControl(''),
  });

  constructor(@Inject(MAT_DIALOG_DATA) public data: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>) {
  }

  showTextAreaReason(deletionVariant) {
    return (this.textFormValue === deletionVariant) && (this.textFormValue === environment.OTHER_REASON);
  }

  onReasonChange(event: MatRadioChange) {
    if (event.value === environment.OTHER_REASON) {
      this.updateOtherControlValidator([Validators.required, Validators.maxLength(InputLengths.about)]);
    } else {
      this.updateOtherControlValidator();
    }
  }

  deleteWithReason(deletionForm) {
    let resultData;
    if (deletionForm.value.text === environment.OTHER_REASON) {
      resultData = {text: deletionForm.value.other};
    } else {
      resultData = {text: deletionForm.value.text};
    }
    this.confirmed.emit(resultData);
  }

  private updateOtherControlValidator(validators?: ValidatorFn | ValidatorFn[]) {
    validators ? this.deletionForm.controls.other.setValidators(validators) : this.deletionForm.controls.other.clearValidators();
    this.deletionForm.controls.other.updateValueAndValidity();
  }

  private get textFormValue() {
    return this.deletionForm.value.text;
  }
}
