import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreState } from '../../core/states/core.state';
import { LocationFilterService } from '../../shared/services/location-filter.service';
import { ViewJobSeekerListPageActions } from '../actions';
import { JobSeekerListMode, LocationSearchFilter } from '../models/job-seeker-list-fitlers.model';


@Injectable()
export class ViewJobSeekersListResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    const search = this.store.selectSnapshot(CoreState.globalSearchParam);
    const location = this.store.selectSnapshot(CoreState.globalLocationSearchParam);
    const searchParams = {};
    if (search) {
      Object.assign(searchParams, {
        search
      });
    }
    if (location) {
      const filter = LocationFilterService.getLocationFilter(LocationSearchFilter, location);
      this.store.dispatch(new ViewJobSeekerListPageActions.SetGlobalFilterOnInit(filter));
      Object.assign(searchParams, {
        location: location.name
      });
    }
    return this.store.dispatch(
      new ViewJobSeekerListPageActions.InitJobSeekerList(JobSeekerListMode.ALL, {...searchParams}));
  }
}
