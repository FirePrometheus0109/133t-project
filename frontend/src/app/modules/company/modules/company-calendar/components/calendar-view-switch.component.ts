import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CalendarView } from 'angular-calendar';

@Component({
  selector: 'cc-calendar-view-switch',
  template: `
  <mat-card>
    <mat-button-toggle-group [value]="view" aria-label="Schedule">
      <mat-button-toggle
        *ngFor="let optView of calendarViews"
        [value]="optView"
        (click)="change.emit(optView)"
      >
        {{optView | titlecase}}
      </mat-button-toggle>
    </mat-button-toggle-group>
  </mat-card>
  `
})
export class CalendarViewSwitchComponent {
  public readonly calendarViews = [CalendarView.Month, CalendarView.Day];

  @Input() view: CalendarView;
  @Output() change = new EventEmitter<CalendarView>();
}
