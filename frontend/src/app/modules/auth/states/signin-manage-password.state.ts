import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { SigninManagePasswordActions } from '../actions';
import { AuthenticationService } from '../services';


class SigninManagePasswordStateModel {
  status: string;
  errors: object;
  token: string;
  user: number;
  invitationMode: boolean;
}


const SIGNIN_MANAGE_PASSWORD_DEFAULT_STATE = {
  status: null,
  errors: null,
  token: '',
  user: null,
  invitationMode: false
};


@State<SigninManagePasswordStateModel>({
  name: 'signinManagePassword',
  defaults: SIGNIN_MANAGE_PASSWORD_DEFAULT_STATE,
})
export class SigninManagePasswordState {
  @Selector()
  static token(state: any) {
    return state.token;
  }

  @Selector()
  static user(state: any) {
    return state.user;
  }

  @Selector()
  static invitationMode(state: any) {
    return state.invitationMode;
  }

  constructor(private navigationService: NavigationService,
              private authService: AuthenticationService) {
  }

  @Action(SigninManagePasswordActions.RestoreAccount)
  restoreAccount(ctx: StateContext<SigninManagePasswordStateModel>, {restoreData}: SigninManagePasswordActions.RestoreAccount) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.authService.restoreAccount(restoreData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'Your account was successfully restored',
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
        return setTimeout(() => this.navigationService.goToLoginPage());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(SigninManagePasswordActions.SetParams)
  setParams(ctx: StateContext<SigninManagePasswordStateModel>, {params}: SigninManagePasswordActions.SetParams) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      token: params.token,
      user: params.user,
    });
  }

  @Action(SigninManagePasswordActions.SetInvitationMode)
  setInvitationMode(ctx: StateContext<SigninManagePasswordStateModel>,
                    {value}: SigninManagePasswordActions.SetInvitationMode) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      invitationMode: value,
    });
  }

  @Action(SigninManagePasswordActions.SetPasswordForInvitedUser)
  setPasswordForInvitedUser(ctx: StateContext<SigninManagePasswordStateModel>,
                            {params}: SigninManagePasswordActions.SetPasswordForInvitedUser) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.authService.setInvitedUserPassword(params).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'Done',
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
        return setTimeout(() => this.navigationService.goToLoginPage());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }
}
