import { Component, EventEmitter, Output } from '@angular/core';


@Component({
  selector: 'app-stop-job-dialog',
  template: `
    <mat-dialog-content align="center">
      As you stopped the job from applying, the next job has been added to application list:
      <div (click)="showNextJob.emit()" class="link">
        View next job details
      </div>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button [mat-dialog-close]>Close</button>
    </mat-dialog-actions>
  `,
  styles: []
})
export class StopJobDialogComponent {
  @Output() showNextJob = new EventEmitter<any>();
}
