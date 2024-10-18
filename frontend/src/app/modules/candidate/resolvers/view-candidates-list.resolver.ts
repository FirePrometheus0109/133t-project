import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { ViewCandidateListPageActions } from '../actions';
import { CandidateListMode } from '../models/candidate-parametr.model';


@Injectable()
export class ViewCandidatesListResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    return this.store.dispatch(
      new ViewCandidateListPageActions.InitCandidateList(CandidateListMode.ALL_CANDIDATE));
  }
}
