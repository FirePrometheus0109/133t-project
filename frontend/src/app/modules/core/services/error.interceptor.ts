import {
  HTTP_INTERCEPTORS,
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Store } from '@ngxs/store';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/internal/operators';
import { environment } from '../../../../environments/environment';
import { AuthState } from '../../auth/states/auth.state';
import { HttpStatuses } from '../../shared/constants/http-statuses';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { CoreActions } from '../actions';
import { ErrorService } from './error.service';
import { NavigationService } from './navigation.service';


/**
 * Intercepts the HTTP responses, and in case that an error/exception is thrown, handles it
 * and extract the relevant information of it.
 */
@Injectable({
  providedIn: 'root'
})
export class ErrorInterceptor implements HttpInterceptor {
  private readonly ignoringCheckers = {
    refreshHasExpired: errorResponse => {
      return errorResponse.error.non_field_errors
        ? errorResponse.error.non_field_errors.includes('Refresh has expired.')
        : false;
    },
    signatureHasExpired: errorResponse => {
      return errorResponse.error.non_field_errors
        ? errorResponse.error.non_field_errors.includes('Signature has expired.')
        : false;
    }
  };

  constructor(private store: Store, private errorService: ErrorService, private navigationService: NavigationService) {
  }

  private shouldErrorBeIgnored(error): boolean {
    return Object.keys(this.ignoringCheckers)
      .map(
        (key): boolean => {
          return this.ignoringCheckers[key](error);
        }
      )
      .includes(true);
  }

  private redirectWithSubscriptionExpiration(error) {
    if (error.error.errors &&
      error.error.errors.includes(environment.expiredSubscriptionResponse) &&
      this.store.selectSnapshot(AuthState.isSubscriptionExpired)) {
      this.navigationService.goToCompanyDashboardPage();
    } else if (error.error.errors && error.error.errors.includes(environment.expiredSubscriptionResponse)) {
      this.store.dispatch(new CoreActions.UpdateUserPlanSubscription());
    }
  }

  intercept(request: HttpRequest<any>,
            next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError(error => {
        if (error instanceof HttpErrorResponse) {
          if (!this.shouldErrorBeIgnored(error)) {
            this.store.dispatch(
              new CoreActions.SnackbarOpen({
                message: this.errorService.handleErrorMessage(error),
                delay: environment.snackBarDelay,
                type: SnackBarMessageType.ERROR
              })
            );

            switch (error.status) {
              case HttpStatuses['400_BAD_REQUEST']: {
                this.store.dispatch(new CoreActions.AddHttpError400(error));
                break;
              }
              case HttpStatuses['401_UNAUTHORIZED']: {
                this.store.dispatch(new CoreActions.AddHttpError401(error));
                break;
              }
              case HttpStatuses['403_FORBIDDEN']: {
                // always redirect to company dashboard to provide purchase subscription
                this.redirectWithSubscriptionExpiration(error);
                this.store.dispatch(new CoreActions.AddHttpError403(error));
                break;
              }
              case HttpStatuses['404_NOT_FOUND']: {
                this.store.dispatch(new CoreActions.AddHttpError404(error));
                break;
              }
              // 500 - Internal Server Error
              case 0: {
                this.store.dispatch(new CoreActions.AddHttpError500(error));
                break;
              }
              case HttpStatuses['500_INTERNAL_SERVER_ERROR']: {
                this.store.dispatch(new CoreActions.AddHttpError500(error));
                break;
              }
              // All Another Errors
              default: {
                this.store.dispatch(new CoreActions.AddHttpErrorAny(error));
                break;
              }
            }
          }
          return throwError(error);
        }
      })
    );
  }
}


/**
 * Provider POJO for the interceptor
 */
export const ErrorInterceptorProvider = {
  provide: HTTP_INTERCEPTORS,
  useClass: ErrorInterceptor,
  multi: true
};
