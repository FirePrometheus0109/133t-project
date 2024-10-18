import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthRoute } from '../../shared/constants/routes/auth-routes';
import { SigninManagePasswordActions } from '../actions';


@Injectable()
export class InvitedCompanySignupResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<void> {
    return this.store.dispatch(new SigninManagePasswordActions
      .SetInvitationMode(route.routeConfig.path.includes(AuthRoute.invitedSignupRoute)));
  }
}
