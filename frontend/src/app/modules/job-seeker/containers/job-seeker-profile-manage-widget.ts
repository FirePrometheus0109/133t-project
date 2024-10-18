import {Component} from '@angular/core';
import {Store} from '@ngxs/store';

// TODO: fill this component with components for the widget, when they are ready.
@Component({
  selector: 'app-job-seeker-profile-manage-widget',
  template: `
    <mat-card>
      <mat-card-content>
        <ng-content select="body"></ng-content>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class JobSeekerProfileManageWidgetComponent {

  constructor(private store: Store) {
  }
}
