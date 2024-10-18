import { Component, EventEmitter, Output } from '@angular/core';

import { ViewDateSwitchDirection } from '../states/calendar.state';

@Component({
  selector: 'cc-calendar-date-changer',
  template: `
  <mat-card>
    <button mat-button color="primary" (click)="change.emit(ViewDateSwitchDirection.Previous)">Prev</button>
    <button mat-fab color="primary" (click)="change.emit(ViewDateSwitchDirection.Today)">Today</button>
    <button mat-button color="primary" (click)="change.emit(ViewDateSwitchDirection.Next)">Next</button>
  </mat-card>
  `
})
export class CalendarDateChangerComponent {
  public readonly ViewDateSwitchDirection = ViewDateSwitchDirection;
  @Output() change = new EventEmitter<ViewDateSwitchDirection>();
}
