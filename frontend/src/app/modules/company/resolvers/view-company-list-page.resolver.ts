import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { ViewCompanyListPageActions } from '../actions';


@Injectable()
export class ViewCompanyListPageResolver implements Resolve<Observable<any>> {
  readonly listLimit = 100;

  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    return this.store.dispatch(new ViewCompanyListPageActions.LoadCompaniesData(this.listLimit, 0));
  }
}
