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
import { tap } from 'rxjs/operators';
import { CoreActions } from '../actions';


@Injectable({
  providedIn: 'root',
})
export class LoaderInterceptor implements HttpInterceptor {
  constructor(private store: Store) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req)
      .pipe(
        tap(
          () => this.showLoader(),
          () => this.onEnd(),
          () => this.onEnd()
        )
      );
  }

  private onEnd(): void {
    this.hideLoader();
  }

  private showLoader(): void {
    this.store.dispatch(new CoreActions.ShowLoader());
  }

  private hideLoader(): void {
    this.store.dispatch(new CoreActions.HideLoader());
  }
}


/**
 * Provider POJO for the interceptor
 */
export const LoaderInterceptorProvider = {
  provide: HTTP_INTERCEPTORS,
  useClass: LoaderInterceptor,
  multi: true,
};
