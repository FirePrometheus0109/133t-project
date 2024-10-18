import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AutoApplyEditActions } from '../actions';


@Injectable()
export class AutoApplyEditPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    this.store.dispatch(new AutoApplyEditActions.CleanAutoApplyData());
    this.store.dispatch(new AutoApplyEditActions.LoadAutoApplyJobs(route.params.id));
    return this.store.dispatch(new AutoApplyEditActions.LoadAutoApply(route.params.id));
  }
}
