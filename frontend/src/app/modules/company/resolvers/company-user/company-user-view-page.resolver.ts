import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CompanyUserManagePageActions } from '../../actions/index';


@Injectable()
export class CompanyUserViewPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    this.store.dispatch(new CompanyUserManagePageActions.SetViewMode(true));
    this.store.dispatch(new CompanyUserManagePageActions.LoadGroupedPermissions());
    return this.store.dispatch(new CompanyUserManagePageActions.LoadCompanyUserData(route.params.id));
  }
}
