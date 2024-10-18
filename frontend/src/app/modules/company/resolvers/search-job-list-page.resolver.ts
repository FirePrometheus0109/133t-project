import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreState } from '../../core/states/core.state';
import { DEFAULT_PAGINATED_OPTIONS } from '../../shared/models/paginated-data.model';
import { LocationFilterService } from '../../shared/services/location-filter.service';
import { SearchJobListPageActions } from '../actions';
import { LocationSearchFilter } from '../models/jobs-list-filters.model';


@Injectable()
export class SearchJobListPageResolver implements Resolve<Observable<any>> {
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
      this.store.dispatch(new SearchJobListPageActions.SetSelectedFiltersOnInit(filter));
      Object.assign(searchParams, {
        location: filter.value.key
      });
    }
    return this.store.dispatch(new SearchJobListPageActions.LoadJobsData({...DEFAULT_PAGINATED_OPTIONS, ...searchParams}));
  }
}
