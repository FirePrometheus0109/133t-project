import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { Store } from '@ngxs/store';
import { AuthState } from '../../auth/states/auth.state';


@Injectable({
  providedIn: 'root',
})
export class IsJobSeekerGuard implements CanActivate {
  constructor(private store: Store) {
  }

  canActivate(): boolean {
    return this.store.selectSnapshot(AuthState.isJobSeeker);
  }
}
