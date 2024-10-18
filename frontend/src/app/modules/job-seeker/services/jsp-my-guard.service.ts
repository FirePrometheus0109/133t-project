import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate } from '@angular/router';
import { Store } from '@ngxs/store';
import { AuthState } from '../../auth/states/auth.state';
import { NavigationService } from '../../core/services/navigation.service';


@Injectable({
  providedIn: 'root',
})
export class JSPMyGuard implements CanActivate {
  constructor(private store: Store,
              private navigationService: NavigationService) {
  }

  canActivate(route: ActivatedRouteSnapshot): boolean {
    let jobseekerId = route.params.id;
    if (jobseekerId === 'my') {
      jobseekerId = this.store.selectSnapshot(AuthState.jobseekerId);
      this.navigationService.goToJobSeekerProfileEditPage(jobseekerId);
    } else {
      return true;
    }
  }
}
