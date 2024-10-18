import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import * as CoreActions from '../../core/actions/core.actions';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { AccountPageActions } from '../actions';
import { User } from '../models/user.model';
import { AuthenticationService } from '../services';


export class AccountPageStateModel {
  user: User;
  status: string;
  errors: object;
  isEditMode: boolean;
  changedPasswordSuccessMessage: string;
}


const DEFAULT_ACCOUNT_PAGE_STATE = {
  user: null,
  status: null,
  errors: null,
  isEditMode: false,
  changedPasswordSuccessMessage: null,
};


@State<AccountPageStateModel>({
  name: 'AccountPage',
  defaults: DEFAULT_ACCOUNT_PAGE_STATE,
})
export class AccountPageState {
  @Selector()
  static user(state: AccountPageStateModel) {
    return state.user;
  }

  @Selector()
  static pending(state: AccountPageStateModel): boolean {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: AccountPageStateModel): Object {
    return state.errors;
  }

  @Selector()
  static successChangePasswordMessage(state: AccountPageStateModel): string {
    return state.changedPasswordSuccessMessage;
  }

  @Selector()
  static isEditMode(state: AccountPageStateModel): boolean {
    return state.isEditMode;
  }

  constructor(private authService: AuthenticationService) {
  }

  @Action(AccountPageActions.GetAccountData)
  getUserData(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.authService.getUserData().pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          user: result,
          status: 'done',
          errors: null,
        });
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

  @Action(AccountPageActions.UpdateAccountData)
  updateUserData(ctx, {data}: AccountPageActions.UpdateAccountData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.authService.putUserData(data).pipe(
      tap((result) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          user: Object.assign(state.user, result),
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'Data was successfully changed.',
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
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

  @Action(AccountPageActions.UpdateAccountPassword)
  updateAccountPassword(ctx, {data}: AccountPageActions.UpdateAccountPassword) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.authService.updatePassword(data).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          changedPasswordSuccessMessage: result.detail,
          status: 'done',
          errors: null,
        });
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

  @Action(AccountPageActions.ToggleEditMode)
  toggleEditMode(ctx, {isEdit}: AccountPageActions.ToggleEditMode) {
    const state = ctx.getState();
    return of(ctx.setState({
      ...state,
      isEditMode: isEdit,
    }));
  }
}
