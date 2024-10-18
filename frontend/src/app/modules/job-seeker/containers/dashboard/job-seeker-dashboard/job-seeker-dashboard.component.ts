import { Component, OnDestroy } from '@angular/core';
import { Store } from '@ngxs/store';
import { AuthState } from '../../../../auth/states/auth.state';
import { CoreActions } from '../../../../core/actions';
import { NavigationService } from '../../../../core/services/navigation.service';


@Component({
  selector: 'app-job-seeker-dashboard',
  templateUrl: './job-seeker-dashboard.component.html',
  styleUrls: ['./job-seeker-dashboard.component.scss']
})
export class JobSeekerDashboardComponent implements OnDestroy {

  constructor(private navigationService: NavigationService, private store: Store) {
  }

  ngOnDestroy() {
    this.store.dispatch(new CoreActions.ListFavoriteJobs(this.store.selectSnapshot(AuthState.jobseekerId)));
  }

  public goToSavedJobsList() {
    this.navigationService.goToJobSeekerSavedJobs();
  }
}
