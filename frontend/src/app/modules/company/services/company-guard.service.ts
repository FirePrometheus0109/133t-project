import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate } from '@angular/router';
import { Store } from '@ngxs/store';
import { AuthState } from '../../auth/states/auth.state';
import { CoreActions } from '../../core/actions';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';


@Injectable({
  providedIn: 'root',
})
export class CompanyGuard implements CanActivate {
  constructor(private store: Store) {
  }

  canActivate(route: ActivatedRouteSnapshot): boolean {
    const isCompanyUser = this.store.selectSnapshot(AuthState.isCompanyUser);
    if (isCompanyUser) {
      return true;
    } else {
      this.store.dispatch(new CoreActions.SnackbarOpen({
        message: 'Only Company User can create a Job!',
        type: SnackBarMessageType.ERROR,
      }));
      return false;
    }
  }
}
