import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { SavedQuestionsActions } from '../actions';


@Injectable()
export class SavedQuestionsPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    return this.store.dispatch(new SavedQuestionsActions.LoadSavedQuestionList(DEFAULT_PAGINATED_STATE.pageSize, 0));
  }
}
