import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { AutoApplyListActions } from '../actions';

export const INITIAL_TASKS = [
  AutoApplyListActions.LoadAutoApplyList
];


@Injectable()
export class AutoApplyListPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    const tasks$ = [];
    INITIAL_TASKS.forEach(task => tasks$.push(this.store.dispatch(new task())));
    /* tslint:disable */
    return forkJoin(...tasks$);
    /* tslint:enable */
  }
}
