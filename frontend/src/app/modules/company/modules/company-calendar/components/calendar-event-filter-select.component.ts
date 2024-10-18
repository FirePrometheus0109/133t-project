import { Component, EventEmitter, Input, Output } from '@angular/core';

import { CalendarFilterValue } from '../states/calendar.state';

@Component({
  selector: 'cc-calendar-event-filter-select',
  template: `
  <mat-form-field>
    <mat-select [value]="value" (selectionChange)="onChange($event)">
      <mat-option *ngFor="let option of options" [value]="option">
        {{option}}
      </mat-option>
    </mat-select>
  </mat-form-field>
  `
})
export class CalendarEventFilterSelectComponent {
  public options = [CalendarFilterValue.All, CalendarFilterValue.OnlyMy];

  @Input() value: CalendarFilterValue;
  @Output() change = new EventEmitter<CalendarFilterValue>();

  onChange({value}) {
    this.change.emit(value);
  }
}
