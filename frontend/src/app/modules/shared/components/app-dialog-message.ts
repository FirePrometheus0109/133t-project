import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

@Component({
  selector: 'app-message-dialog',
  template: `
    <h1 mat-dialog-title>Info</h1>
    <mat-dialog-content>
      {{message}}
    </mat-dialog-content>
    <mat-dialog-actions>
      <button mat-button [mat-dialog-close]>Got It</button>
    </mat-dialog-actions>
  `,
  styles: []
})
export class AppMessageDialogComponent implements OnInit {
  message: string;

  constructor(@Inject(MAT_DIALOG_DATA) private data,
              public dialogRef: MatDialogRef<AppMessageDialogComponent>) {
  }

  ngOnInit() {
    this.message = this.data.message;
  }
}
