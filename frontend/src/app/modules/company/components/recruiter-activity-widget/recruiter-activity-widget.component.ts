import { Component } from '@angular/core';
import { Select, } from '@ngxs/store';
import { Observable } from 'rxjs';
import { UserActivityData } from '../../models/company-reports.model';
import { CompanyReportsState } from '../../states/company-reports.state';

@Component({
  selector: 'app-recruiter-activity-widget',
  templateUrl: './recruiter-activity-widget.component.html',
  styleUrls: ['./recruiter-activity-widget.component.css']
})
export class RecruiterActivityWidgetComponent {
  @Select(CompanyReportsState.recruiterActivityData) data$: Observable<UserActivityData>;
}
