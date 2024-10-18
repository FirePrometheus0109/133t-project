import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AccountPageActions } from '../actions';


@Injectable()
export class AccountPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    return this.store.dispatch(new AccountPageActions.GetAccountData());
  }
}
