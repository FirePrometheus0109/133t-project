import { Component } from '@angular/core';
import { PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../../../core/services/navigation.service';
import { GridViewHelper } from '../../../../shared/helpers/grid-view.helper';
import { CompanyDashboardActions } from '../../../actions';
import { CandidateActivityModel } from '../../../models/candidate-activity.model';
import { CompanyDashboardState } from '../../../states/company-dashboard.state';


@Component({
  selector: 'app-dashboard-candidates-activity',
  templateUrl: './dashboard-candidates-activity.component.html',
  styleUrls: ['./dashboard-candidates-activity.component.scss']
})
export class DashboardCandidatesActivityComponent {
  @Select(CompanyDashboardState.count) count$: Observable<number>;
  @Select(CompanyDashboardState.pageSize) pageSize$: Observable<number>;
  @Select(CompanyDashboardState.pageSizeOptions) pageSizeOptions$: Observable<Array<number>>;
  @Select(CompanyDashboardState.candidatesActivity) candidatesActivity$: Observable<CandidateActivityModel[]>;

  params = {};

  constructor(private store: Store, private navigationService: NavigationService) {
  }

  public navigateToCandidate(candidateId: number) {
    this.navigationService.goToCandidateProfileViewPage(candidateId.toString());
  }

  public navigateToJob(jobId: number) {
    this.navigationService.goToCompanyJobViewDetailsPage(jobId.toString());
  }

  public onPageChanged(event: PageEvent) {
    GridViewHelper.updatePageParams(this.params, event);
    this.store.dispatch(new CompanyDashboardActions.SetCurrentPagination(this.params));
    this.store.dispatch(new CompanyDashboardActions.LoadCandidatesActivity(this.params));
  }
}
