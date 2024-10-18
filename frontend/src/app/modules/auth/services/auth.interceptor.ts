import {
  HTTP_INTERCEPTORS,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { concatMap } from 'rxjs/operators';

import { PUBLIC_ROUTE } from '../../shared/services/public-api.service';
import { RefreshToken } from '../actions/auth.actions';
import { AuthState } from '../states/auth.state';

import { environment } from '../../../../environments/environment';
import { millisecondsInSecond } from '../../shared/constants/technical-values';

@Injectable()
export class JWTTokenInterceptor implements HttpInterceptor {
  /**
   * Observable that containing in the head a token update event to which
   * requests are connected waiting for the token permission
   */
  private refreshLocker$: Observable<any>;
  /**
   * Min time in seconds, if less than - inteceptor should refresh token if possible.
   */
  readonly refreshIfLessThan = environment.minTimeBeforeTokenWillBeExpiredWithoutRefresh; // seconds
  readonly ignoredRoutesContains = ['/api-token-refresh'];

  constructor(private store: Store) {}
  /**
   * Check for "public" prefix in route.
   * @param  {HttpRequest<any>} request
   * @returns boolean
   */
  private checkIsPublicRoute(request: HttpRequest<any>): boolean {
    return !request.url.includes(`/${PUBLIC_ROUTE}/`);
  }
  /**
   * Make clone of request and adding "Authorization" header.
   * @param  {HttpRequest<any>} request
   * @param  {string} token
   */
  private setAuthHeaderToRequest(request: HttpRequest<any>, token: string) {
    if (token && this.checkIsPublicRoute(request)) {
      return request.clone({
        setHeaders: { Authorization: `JWT ${token}` }
      });
    }
    return request;
  }
  /**
   * Contains additional request setup, for now
   * it disable withCredentails option on request.
   * Return modified clone of request.
   * @param  {HttpRequest<any>} request
   */
  private makeDefaultRequestSetup(request: HttpRequest<any>) {
    return request.clone({ withCredentials: false });
  }
  /**
   * Returns the rest of received time in seconds from now.
   * @param {number} expireAtSec - Expiration date in seconds
   * @returns number
   */
  private getExpiredInTimeFromNow(expireAtSec: number): number {
    if (expireAtSec) {
      const diff = expireAtSec - new Date().getTime() / millisecondsInSecond;
      if (diff > 0) { return diff; }
    }
    return 0;
  }
  /**
   * Check - should we processed received request or just pass.
   * @param request
   * @return {boolean}
   */
  private checkIfShouldIntercept(request: HttpRequest<any>): boolean {
    if (!this.checkIsPublicRoute(request)) {
      return false;
    }
    for (const ignoredRoute of this.ignoredRoutesContains) {
      if (request.url.includes(ignoredRoute)) {
        return false;
      }
    }
    return true;
  }
  /**
   * It takes secconds before expiring and compares with the parameter from "environment"
   * @param  {number} expiredInSeconds
   * @returns boolean
   */
  private checkIfTokenExpireSoon(expiredInSeconds: number): boolean {
    return expiredInSeconds < this.refreshIfLessThan;
  }
  /**
   * Return working data from store by snapshot.
   * @returns object
   */
  private getRelatedDataFromStoreSync(): {
    refreshingLock: boolean,
    JWTToken: string,
    JWTTokenExpiresAt: number
  } {
    return {
      refreshingLock: this.store.selectSnapshot<boolean>(
        AuthState.refreshingTokenLock
      ),
      JWTToken: this.store.selectSnapshot<string>(AuthState.token),
      JWTTokenExpiresAt: this.store.selectSnapshot<number>(AuthState.expiresAt)
    };
  }

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {

    // Getting working data.
    const {
      refreshingLock,
      JWTToken,
      JWTTokenExpiresAt
    } = this.getRelatedDataFromStoreSync();

    // Prepare request, adding auth headers.
    const patchedRequest = this.makeDefaultRequestSetup(
      this.setAuthHeaderToRequest(request, JWTToken)
    );

    // Define - did interceptor will process current request.
    const shouldIntercept = JWTToken
      ? this.checkIfShouldIntercept(patchedRequest)
      : false;

    // Contain current time in seconds before expiring.
    const expiredInSeconds = this.getExpiredInTimeFromNow(JWTTokenExpiresAt);
    const didTokenExpireSoon = this.checkIfTokenExpireSoon(expiredInSeconds);

    // Check did we need to update token.
    if (shouldIntercept && didTokenExpireSoon) {
      // If token is not already updating
      if (!refreshingLock) {
        // Make head event - "refreshing token"
        this.refreshLocker$ = this.store.dispatch(new RefreshToken(JWTToken));
      }
      // Add current request to queue, patching request with new token(possibly)
      return this.refreshLocker$.pipe(
        concatMap(_ => {
          const { JWTToken: token } = this.getRelatedDataFromStoreSync();
          return next.handle(
            this.setAuthHeaderToRequest(patchedRequest, token)
          );
        })
      );
    }
    // Pass if we don't need to make any actions and token is valid
    return next.handle(patchedRequest);
  }
}

export const JWTTokenInterceptorProvider = {
  provide: HTTP_INTERCEPTORS,
  useClass: JWTTokenInterceptor,
  multi: true
};
