import { Component, Input } from '@angular/core';
import { PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../../auth/states/auth.state';
import { CoreActions } from '../../../core/actions';
import { NavigationService } from '../../../core/services/navigation.service';
import { CoreState } from '../../../core/states/core.state';


@Component({
  selector: 'app-job-seeker-saved-jobs-list',
  templateUrl: './job-seeker-saved-jobs-list.component.html',
  styleUrls: ['./job-seeker-saved-jobs-list.component.css']
})
export class JobSeekerSavedJobsListComponent {
  @Select(CoreState.favoriteJobs) favoriteJobs$: Observable<any>;
  @Select(CoreState.favoriteJobsCount) favoriteJobsCount$: Observable<any>;
  @Select(CoreState.favoriteJobsPageSize) favoriteJobsPageSize$: Observable<any>;
  @Select(CoreState.pageSizeOptions) pageSizeOptions$: Observable<any>;
  @Select(CoreState.enums) enums$: Observable<object>;

  @Input() isDashboard: boolean;

  private params = {};

  private static getPaginationParams(paginatedData: PageEvent): object {
    return {
      limit: paginatedData.pageSize,
      offset: paginatedData.pageIndex * paginatedData.pageSize,
    };
  }

  constructor(private store: Store,
              private navigationService: NavigationService) {
  }

  public onPageChanged(paginationData: PageEvent) {
    this.updatePageParams(JobSeekerSavedJobsListComponent.getPaginationParams(paginationData));
    this.store.dispatch(new CoreActions.ListFavoriteJobs(this.store.selectSnapshot(AuthState.jobseekerId), this.params));
  }

  public goToCompanyProfile(companyId: number) {
    this.navigationService.goToCompanyProfileViewPage(companyId.toString());
  }

  public goToJobPage(jobId: number) {
    this.navigationService.goToCompanyJobViewDetailsPage(jobId.toString());
  }

  private updatePageParams(params: object) {
    this.params = Object.assign(this.params, params);
  }
}
