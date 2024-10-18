import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { ManageSubsctiptionActions, SetSubscriptionActions } from '../actions';

@Injectable()
export class ManageSubsctiptionResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve() {
    return forkJoin(
        this.store.dispatch(new ManageSubsctiptionActions.PaymentHistory()),
          this.store.dispatch(new SetSubscriptionActions.LoadCurrentPlan())
      );
  }
}
