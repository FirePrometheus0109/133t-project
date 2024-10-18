import { HttpErrorResponse } from '@angular/common/http';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { ResetUserPasswordActions } from '../actions';
import { AuthenticationService } from '../services/authentication.service';


class ResetUserPasswordStateModel {
  status: string;
  errors: object;
  temporaryEmail: object;
}


export const DEFAULT_RESET_USER_PASSWORD_STATE = {
  status: '',
  errors: null,
  temporaryEmail: {
    email: ''
  },
};


@State<ResetUserPasswordStateModel>({
  name: 'ResetUserPasswordState',
  defaults: DEFAULT_RESET_USER_PASSWORD_STATE,
})
export class ResetUserPasswordState {
  @Selector()
  static errors(state: ResetUserPasswordStateModel): object {
    return state.errors;
  }

  @Selector()
  static temporaryEmail(state: ResetUserPasswordStateModel): object {
    return state.temporaryEmail;
  }

  constructor(private authService: AuthenticationService,
              private navigationService: NavigationService) {
  }

  @Action(ResetUserPasswordActions.SetTemporaryEmailField)
  setTemporaryEmailField(ctx: StateContext<ResetUserPasswordStateModel>,
                         {email}: ResetUserPasswordActions.SetTemporaryEmailField) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      temporaryEmail: {email},
    });
  }

  @Action(ResetUserPasswordActions.SendForgotPassword)
  sendForgotPassword(ctx: StateContext<ResetUserPasswordStateModel>, {email}: ResetUserPasswordActions.SendForgotPassword) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.authService.sendForgotPassword(email).pipe(
      tap((result) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null
        });
        this.navigationService.goToHomePage();
        return this.showSuccessSnackBar(ctx, result.detail);
      }),
      catchError(error => {
        return this.stateErrorHandler(ctx, error);
      }),
    );
  }

  @Action(ResetUserPasswordActions.ConfirmResetPassword)
  confirmResetPassword(ctx: StateContext<ResetUserPasswordStateModel>, {params}: ResetUserPasswordActions.ConfirmResetPassword) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.authService.confirmResetPassword(params).pipe(
      tap((result) => {
        return this.manageSetPasswordRequest(ctx, result.detail);
      }),
      catchError(error => {
        return this.stateErrorHandler(ctx, error);
      }),
    );
  }

  @Action(ResetUserPasswordActions.SetPassword)
  setPassword(ctx: StateContext<ResetUserPasswordStateModel>, {passwords}: ResetUserPasswordActions.SetPassword) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.authService.setPassword(passwords).pipe(
      tap((result) => {
        return this.manageSetPasswordRequest(ctx, result.detail);
      }),
      catchError(error => {
        return this.stateErrorHandler(ctx, error);
      }),
    );
  }

  private manageSetPasswordRequest(ctx: StateContext<ResetUserPasswordStateModel>, message: string) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'done',
      errors: null
    });
    this.navigationService.goToHomePage();
    return this.showSuccessSnackBar(ctx, message);
  }

  private showSuccessSnackBar(ctx: StateContext<ResetUserPasswordStateModel>, message: string) {
    return ctx.dispatch(new CoreActions.SnackbarOpen({
      message: message,
      delay: environment.snackBarDelay,
      type: SnackBarMessageType.SUCCESS,
    }));
  }

  private stateErrorHandler(ctx: StateContext<ResetUserPasswordStateModel>, error: HttpErrorResponse) {
    const state = ctx.getState();
    return of(ctx.setState({
      ...state,
      status: 'error',
      errors: error.error
    }));
  }
}
