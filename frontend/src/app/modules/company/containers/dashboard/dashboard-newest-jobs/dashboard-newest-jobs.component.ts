import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../../../auth/states/auth.state';
import { NavigationService } from '../../../../core/services/navigation.service';
import { CoreState } from '../../../../core/states/core.state';
import { JobItem } from '../../../models/job.model';
import { CompanyDashboardState } from '../../../states/company-dashboard.state';


@Component({
  selector: 'app-dashboard-newest-jobs',
  templateUrl: './dashboard-newest-jobs.component.html',
  styleUrls: ['./dashboard-newest-jobs.component.scss']
})
export class DashboardNewestJobsComponent {
  @Select(CoreState.enums) enums$: Observable<object>;
  @Select(AuthState.isCompanyUser) isCompanyUser$: Observable<boolean>;
  @Select(CompanyDashboardState.newestJobs) newestJobs$: Observable<JobItem[]>;

  constructor(private navigationService: NavigationService) {
  }

  public navigateToJobsList() {
    this.navigationService.goToCompanyJobListPage();
  }

  public navigateToJob(jobId: number) {
    this.navigationService.goToCompanyJobViewDetailsPage(jobId.toString());
  }
}
