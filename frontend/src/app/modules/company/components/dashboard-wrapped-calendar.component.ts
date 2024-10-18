import { Component } from '@angular/core';


@Component({
  selector: 'company-dashboard-wrapped-calendar',
  template: `
    <mat-card>
      <app-score-card-stats></app-score-card-stats>
    </mat-card>
    <cc-calendar></cc-calendar>
  `,
  styles: []
})
export class DashboardWrappedCalendarComponent {}
