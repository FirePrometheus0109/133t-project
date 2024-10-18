import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { ViewJobDetailsJSPageActions } from '../actions';


@Injectable()
export class ViewJobDetailsJsPublicPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    return this.store.dispatch(new ViewJobDetailsJSPageActions.LoadPublicJobData(route.params.uid));
  }
}
