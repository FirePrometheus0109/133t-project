import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { CompanyReportsActions } from '../actions';


@Injectable()
export class CompanyReportsResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve() {
    const companyId = this.store.selectSnapshot(AuthState.companyId);
    return forkJoin(this.store.dispatch(new CompanyReportsActions.InitCompanyId(companyId)),
    this.store.dispatch(new CompanyReportsActions.InitReportData()));
  }
}
