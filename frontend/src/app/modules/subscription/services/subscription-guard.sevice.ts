import { Injectable } from '@angular/core';
import { CanActivate, CanDeactivate } from '@angular/router';
import { Store } from '@ngxs/store';
import { AuthState } from '../../auth/states/auth.state';


@Injectable({
  providedIn: 'root',
})
export class IsSubsctiptionPurchased implements CanActivate, CanDeactivate<any> {
  constructor(private store: Store) {
  }

  canActivate(): boolean {
    return this.store.selectSnapshot(AuthState.isSubsctiptionPurchased);
  }

  canDeactivate(): boolean {
    return this.store.selectSnapshot(AuthState.isSubsctiptionPurchased);
  }
}
