import { Component, EventEmitter, Inject, Input, OnInit, Output } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';


@Component({
  selector: 'app-confirmation-dialog',
  template: `
    <h3 mat-dialog-title align="center">{{title}}</h3>
    <mat-dialog-content align="center">
      {{message}}
    </mat-dialog-content>
    <mat-dialog-actions align="center">
      <button mat-raised-button color="primary" (click)="confirmed.emit(true)">
        <mat-icon matSuffix>check</mat-icon>
        {{confirmText}}
      </button>
      <button *ngIf="dismissible" mat-raised-button color="accent" (click)="confirmed.emit(false)">
        <mat-icon matSuffix>close</mat-icon>
        {{negativeText}}
      </button>
    </mat-dialog-actions>
  `,
  styles: []
})
export class ConfirmationDialogComponent implements OnInit {
  @Input() dismissible = true;
  @Output() confirmed = new EventEmitter<boolean>();

  title: string;
  message: string;
  confirmText: string;
  negativeText: string;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>) {
  }

  ngOnInit() {
    this.title = this.data.title;
    this.message = this.data.message;
    this.confirmText = this.data.confirmButtonText;
    this.negativeText = this.data.negativeButtonText;
    this.dismissible = this.data.dismissible;
  }
}
