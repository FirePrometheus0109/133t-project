import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { JobSeekerAutoApplyProgressItem } from '../../../models/job-seeker-auto-apply-progress.model';
import { JobSeekerDashboardState } from '../../../states/job-seeker-dashboard.state';


@Component({
  selector: 'app-job-seeker-auto-apply-progress',
  templateUrl: './job-seeker-auto-apply-progress.component.html',
  styleUrls: ['./job-seeker-auto-apply-progress.component.scss']
})
export class JobSeekerAutoApplyProgressComponent {
  @Select(JobSeekerDashboardState.autoApplyProgressList) autoApplyProgressList$: Observable<JobSeekerAutoApplyProgressItem[]>;
}
