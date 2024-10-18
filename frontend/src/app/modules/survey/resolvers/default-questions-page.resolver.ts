import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { DefaultQuestionsActions } from '../actions';


@Injectable()
export class DefaultQuestionsPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    return this.store.dispatch(new DefaultQuestionsActions.LoadDefaultQuestionList());
  }
}
