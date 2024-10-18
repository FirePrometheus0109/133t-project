import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { JobSeekerDashboardActions } from '../actions';


@Injectable()
export class JobSeekerDashboardPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    if (this.store.selectSnapshot(AuthState.isJobSeeker)) {
      return this.store.dispatch(new JobSeekerDashboardActions.LoadInitialData(this.store.selectSnapshot(AuthState.jobseekerId)));
    }
  }
}
