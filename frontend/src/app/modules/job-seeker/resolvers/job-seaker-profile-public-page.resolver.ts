import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { concat } from 'rxjs';
import { JobSeekerProfilePublicPageActions } from '../actions';

@Injectable()
export class JobSeekerProfilePublicPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    return concat(
      this.store.dispatch(new JobSeekerProfilePublicPageActions.DisplayAsPublic()),
      this.store.dispatch(new JobSeekerProfilePublicPageActions.LoadPublicProfile(route.params.uid))
    );
  }
}
