import { Action, Selector, State, StateContext } from '@ngxs/store';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { AuthActions, VerifyEmailActions } from '../actions';


class VerifyEmailStateModel {
  token?: string;
  pending: boolean;
  verified: boolean;
  result: object;
}


const VERIFY_EMAIL_DEFAULT_STATE = {
  token: null,
  pending: false,
  verified: true,
  result: null,
};


@State<VerifyEmailStateModel>({
  name: 'verifyemail',
  defaults: VERIFY_EMAIL_DEFAULT_STATE,
})
export class VerifyEmailState {
  @Selector()
  static pending(state: any) {
    return state.pending;
  }

  @Selector()
  static verified(state: any) {
    return state.verified;
  }

  constructor(private navigationService: NavigationService) {
  }

  @Action(VerifyEmailActions.VerifyEmail)
  verifyEmail(ctx: StateContext<VerifyEmailStateModel>, {token}: VerifyEmailActions.VerifyEmail) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      token: token,
    });
    return setTimeout(() => ctx.dispatch(new AuthActions.VerifyEmail(token)));
  }

  @Action(VerifyEmailActions.VerifyEmailResult)
  verifyEmailResult(ctx: StateContext<VerifyEmailStateModel>, {result}: VerifyEmailActions.VerifyEmailResult) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      result: result,
    });
    if (result['detail']) {
      state = ctx.getState();
      ctx.setState({
        ...state,
        verified: true,
        pending: false,
      });
      ctx.dispatch(new CoreActions.SnackbarOpen({
        message: result['detail'],
        delay: 5000,
        type: SnackBarMessageType.SUCCESS,
      }));
      return setTimeout(() => this.navigationService.goToLoginPage());
    } else {
      state = ctx.getState();
      ctx.setState({
        ...state,
        verified: false,
        pending: false,
      });
      ctx.dispatch(new CoreActions.SnackbarOpen({
        message: result['detail'],
        delay: 5000,
        type: SnackBarMessageType.WARNING,
      }));
    }
  }
}
