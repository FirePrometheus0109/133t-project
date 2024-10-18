import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate } from '@angular/router';
import { Store } from '@ngxs/store';
import { AuthState } from '../../auth/states/auth.state';
import { NavigationService } from '../../core/services/navigation.service';


@Injectable({
  providedIn: 'root',
})
export class CompanyMyGuard implements CanActivate {
  constructor(private store: Store,
              private navigationService: NavigationService) {
  }

  canActivate(route: ActivatedRouteSnapshot): boolean {
    let companyId = route.params.id;
    if (companyId === 'my') {
      companyId = this.store.selectSnapshot(AuthState.companyId);
      this.navigationService.goToCompanyProfileEditPage(companyId);
    } else {
      return true;
    }
  }
}
