import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { SetTrialPlanActions } from '../actions';

@Injectable()
export class ViewAvailableTrialPlanListResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    return this.store.dispatch(
      new SetTrialPlanActions.LoadAvailablePlans());
  }
}
