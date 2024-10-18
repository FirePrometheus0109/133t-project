import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreActions } from '../../core/actions';


@Injectable()
export class AppliedJobsListPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    return this.store.dispatch(new CoreActions.LoadAppliedJobs());
  }
}
