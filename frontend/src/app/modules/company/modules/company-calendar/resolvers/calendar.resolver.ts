import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { concat, Observable } from 'rxjs';

import { CalendarActions } from '../actions';


@Injectable()
export class CompanyCalendarPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {}

  resolve(): Observable<void> {
    return concat(
      this.store.dispatch(new CalendarActions.LoadCalendarEvents())
    );
  }
}
