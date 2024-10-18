import { AfterContentInit, Component, Inject } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef, MatSnackBar} from '@angular/material';
import * as copy from 'copy-to-clipboard';
import { tap } from 'rxjs/operators';

import { CompanyRoute } from '../../../shared/constants/routes/company-routes';
import { JobService } from '../../services/job.service';

export interface DialogData {
  uid: string;
  id: number;
}

const copyMessage = 'Job posting link was copied to clipboard.';
const emailSendMessage = 'Job posting link was send to specified email.';
const copyAction = 'Ok, got it';

const moreIconName = 'expand_more';
const lessIconName = 'expand_less';

@Component({
  selector: 'app-share-job-dialog',
  template: `
  <div mat-dialog-content>
    <div fxLayout="row">
      <mat-form-field fxFlex="90">
        <input matInput
              readonly
              placeholder="URL link"
              [value]="shareUrl">
      </mat-form-field>
      <div fxFlex="10" fxLayoutAlign="center center">
        <button mat-button
            matSuffix
            aria-label="Copy"
            (click)="copy()">
          COPY
        </button>
      </div>
    </div>
    <div fxFlexFill
         fxLayout="row"
         fxLayoutAlign="center center">
      <button mat-button
              mat-flat-button
              aria-label="Copy"
              (click)="toggleEmailSharing()">
        <mat-icon matSuffix>mail_outline</mat-icon>
        via email?
      </button>
      <mat-icon>{{getExpandIconName()}}</mat-icon>
    </div>
    <div *ngIf="isEmailSharing"
          fxLayout="row">
      <mat-form-field fxFlex="91%">
        <input matInput
               placeholder="Email to"
               [formControl]="emailCtrl">
      </mat-form-field>
      <div fxFlex="9%" fxLayoutAlign="center center">
        <button mat-button
            matSuffix
            aria-label="Send"
            [disabled]="!emailCtrl.valid"
            (click)="sendEmail()">
          SEND
        </button>
      </div>
    </div>
  </div>
  `,
})
export class ShareJobDialogComponent implements AfterContentInit {
  public shareUrl: string;
  public isEmailSharing = false;
  public snackDuration = 4000;
  public dialogDefaultWidth = '65%';

  public emailCtrl = new FormControl('', [Validators.required, Validators.email]);

  constructor(
    public dialogRef: MatDialogRef<ShareJobDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    private snackBar: MatSnackBar,
    private jobService: JobService
  ) {
    this.shareUrl = CompanyRoute.getPublicJobUrl(this.data.uid);
  }

  ngAfterContentInit(): void {
    this.dialogRef.updateSize(this.dialogDefaultWidth);
  }

  copy() {
    copy(this.shareUrl);
    this.snackBar.open(copyMessage, copyAction, {
      duration: this.snackDuration,
    });
  }

  toggleEmailSharing() {
    this.isEmailSharing = !this.isEmailSharing;
  }

  sendEmail() {
    this.jobService.shareJobByEmail(this.data.id, {email: this.emailCtrl.value, url: this.shareUrl})
      .pipe(
        tap(() => {
          this.snackBar.open(emailSendMessage, copyAction, {
            duration: this.snackDuration,
          });
        })
      )
      .subscribe();
  }

  getExpandIconName() {
    if (this.isEmailSharing) {
      return lessIconName;
    }
    return moreIconName;
  }
}
