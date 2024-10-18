import { Component } from '@angular/core';
import { PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../../../auth/states/auth.state';
import { NavigationService } from '../../../../core/services/navigation.service';
import { GridViewHelper } from '../../../../shared/helpers/grid-view.helper';
import { JobSeekerDashboardActions } from '../../../actions';
import { JobSeekerLastViewsItemModel } from '../../../models/job-seeker-last-views.model';
import { JobSeekerDashboardState } from '../../../states/job-seeker-dashboard.state';


@Component({
  selector: 'app-job-seeker-last-views-list',
  templateUrl: './job-seeker-last-views-list.component.html',
  styleUrls: ['./job-seeker-last-views-list.component.scss']
})
export class JobSeekerLastViewsListComponent {
  @Select(JobSeekerDashboardState.lastViews) lastViews$: Observable<JobSeekerLastViewsItemModel[]>;
  @Select(JobSeekerDashboardState.count) count$: Observable<number>;
  @Select(JobSeekerDashboardState.pageSize) pageSize$: Observable<number>;
  @Select(JobSeekerDashboardState.pageSizeOptions) pageSizeOptions$: Observable<number[]>;

  private params = {};

  constructor(private navigationService: NavigationService,
              private store: Store) {
  }

  goToCompanyProfile(companyId: number) {
    this.navigationService.goToCompanyProfileViewPage(companyId.toString());
  }

  onPageChanged(event: PageEvent) {
    GridViewHelper.updatePageParams(this.params, event);
    this.store.dispatch(new JobSeekerDashboardActions.GetLastViewsList(this.store.selectSnapshot(AuthState.jobseekerId), this.params));
  }
}
