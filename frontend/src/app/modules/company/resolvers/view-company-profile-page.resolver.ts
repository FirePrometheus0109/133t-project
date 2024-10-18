import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { CompanyProfilePageActions } from '../actions';


@Injectable()
export class ViewCompanyProfilePageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    const userPermissions = this.store.selectSnapshot(AuthState.permissions);
    if (userPermissions && userPermissions.find(permission => permission.codename === 'view_job')) {
      this.store.dispatch(new CompanyProfilePageActions.LoadJobsData(route.params.id));
    } else {
      this.store.dispatch(new CompanyProfilePageActions.LoadPublicJobsData(route.params.id));
    }
    return this.store.dispatch(new CompanyProfilePageActions.LoadPublicInitialData(route.params.id));
  }
}
