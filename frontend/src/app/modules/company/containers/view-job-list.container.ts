import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreState } from '../../core/states/core.state';
import { ViewJobListPageState } from '../states/view-job-list-page.state';


@Component({
  selector: 'app-view-job-list-page',
  template: `
    <app-view-job-preview *ngFor="let jobItem of results$ | async"
                          [jobItem]="jobItem"
                          [enums]="enums$ | async"
                          [isEditable]="false">
    </app-view-job-preview>
  `,
  styles: [],
})
export class ViewJobListPageComponent {
  @Select(ViewJobListPageState.results) results$: Observable<any>;
  @Select(CoreState.enums) enums$: Observable<object>;
}
