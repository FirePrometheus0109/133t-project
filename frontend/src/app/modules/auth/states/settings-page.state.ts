import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { NavigationService } from '../../core/services/navigation.service';
import { AuthActions, SettingsPageActions } from '../actions';
import { AuthenticationService } from '../services';


export class SettingsPageStateModel {
  status: string;
  errors: object;
}


const DEFAULT_SETTINGS_PAGE_STATE = {
  status: null,
  errors: null,
};


@State<SettingsPageStateModel>({
  name: 'SettingsPage',
  defaults: DEFAULT_SETTINGS_PAGE_STATE,
})
export class SettingsPageState {
  @Selector()
  static pending(state: SettingsPageStateModel): boolean {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: SettingsPageStateModel): Object {
    return state.errors;
  }

  constructor(private authService: AuthenticationService,
              private navigationService: NavigationService) {
  }

  @Action(SettingsPageActions.DeleteAccount)
  deleteAccount(ctx, {deletionReason}: SettingsPageActions.DeleteAccount) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.authService.deleteAccount(deletionReason).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new AuthActions.CleanAuthData());
        return setTimeout(() => this.navigationService.goToHomePage());
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
