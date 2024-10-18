import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { DEFAULT_PAGINATED_OPTIONS } from '../../shared/models/paginated-data.model';
import { NotificationListActions } from '../actions';


@Injectable()
export class NotificationListResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    return this.store.dispatch(new NotificationListActions.GetFullNotificationList(DEFAULT_PAGINATED_OPTIONS));
  }
}
