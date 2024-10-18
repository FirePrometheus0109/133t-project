import { Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';

import { EventAttendeeStatus } from '../states/event-form-dialog.state';

@Component({
  selector: 'cc-attendees-list',
  template: `
  <div class="cc-attendees-list-wrapper">
    <mat-chip-list class="mat-chip-list-stacked" *ngIf="formCtrl.value">
      <div
        class="cc-attendees-list-item-wrapper"
        *ngFor="let value of formCtrl.value"
        fxLayoutAlign="center center"
      >
        <mat-icon matTooltip="Accepted" *ngIf="value.status === attendeeStatuses.ACCEPTED">check_circle_outline</mat-icon>
        <mat-icon matTooltip="Rejected" *ngIf="value.status === attendeeStatuses.REJECTED" color="warn">remove_circle_outline</mat-icon>
        <mat-chip (removed)="remove(value.value)">
          {{value.title}}
          <mat-icon matChipRemove>cancel</mat-icon>
        </mat-chip>
      </div>
    </mat-chip-list>
  </div>
  `,
  styles: [`
  .cc-attendees-list-wrapper {
    margin-bottom: 20px;
  }
  `]
})
export class AttendeesListComponent {
  @Input() formCtrl: FormControl; // formControl.value required "title" and "value" keys if not null.

  readonly attendeeStatuses = EventAttendeeStatus;

  remove(value) {
    this.formCtrl.setValue(
      this.formCtrl.value.filter(item => item.value !== value)
    );
    if (!this.formCtrl.dirty) {
      this.formCtrl.markAsDirty();
    }
  }
}
