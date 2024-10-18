import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { SurveyListActions } from '../../survey/actions';
import { CreateJobPageActions } from '../actions';


@Injectable()
export class CreateJobPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    this.store.dispatch(new SurveyListActions.SetCurrentSurvey(null));
    this.store.dispatch(new SurveyListActions.SetJobEditMode(true));
    return this.store.dispatch(new CreateJobPageActions.LoadInitialData());
  }
}
