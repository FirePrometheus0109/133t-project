import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { DEFAULT_PAGINATED_OPTIONS } from '../../../shared/models/paginated-data.model';
import { CompanyUserListPageActions } from '../../actions/index';


@Injectable()
export class CompanyUserListPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    return this.store.dispatch(new CompanyUserListPageActions.LoadCompanyUsersData(DEFAULT_PAGINATED_OPTIONS));
  }
}
