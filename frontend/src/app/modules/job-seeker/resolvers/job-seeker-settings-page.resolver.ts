import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { ManageNotificationsActions } from '../../notifications/actions';


@Injectable()
export class JobSeekerSettingsPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    return this.store.dispatch(new ManageNotificationsActions.GetNotificationsTypes());
  }
}
