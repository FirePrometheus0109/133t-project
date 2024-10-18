import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  CanDeactivate,
  RouterStateSnapshot,
  UrlTree
} from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from '../../auth/states/auth.state';
import { SubscriptionRoute } from '../../shared/constants/routes/subscription-routes';
import { CompanyDashboardComponent } from '../containers/dashboard/company-dashboard/company-dashboard.component';


@Injectable({
  providedIn: 'root',
})
export class CompanySubscriptionGuardService implements CanDeactivate<CompanyDashboardComponent> {

  constructor(private store: Store) {
  }

  canDeactivate(component: CompanyDashboardComponent,
                currentRoute: ActivatedRouteSnapshot,
                currentState: RouterStateSnapshot,
                nextState: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    if (nextState.url === `/${SubscriptionRoute.getFullPaymentRoute()}`) {
      return true;
    }
    return !this.store.selectSnapshot(AuthState.isSubscriptionExpired);
  }
}
