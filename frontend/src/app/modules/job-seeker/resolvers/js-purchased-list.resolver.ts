import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { ViewJobSeekerListPageActions } from '../actions';
import { JobSeekerListMode } from '../models/job-seeker-list-fitlers.model';

@Injectable()
export class ViewPurchasedJobSeekersListResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    return this.store.dispatch(
      new ViewJobSeekerListPageActions.InitJobSeekerList(JobSeekerListMode.PURCHASED));
  }
}
