import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { withLatestFrom } from 'rxjs/operators';
import { AuthActions } from '../actions';
import { AuthState } from '../states/auth.state';


@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  @Select(AuthState.token) token$: Observable<string>;

  constructor(private store: Store) {
  }

  canActivate(): boolean {
    return this.store.selectSnapshot<boolean>(() => {
      const JWTToken = this.store.selectSnapshot<string>(AuthState.token);
      if (!JWTToken) {
        return false;
      } else {
        this.store.dispatch(new AuthActions.VerifyToken(JWTToken)).pipe(
          withLatestFrom(this.token$),
        ).subscribe((res) => {
          if (!res[1]) {
            return false;
          }
        });
      }
      return true;
    });
  }
}
