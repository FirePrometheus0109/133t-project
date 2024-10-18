import { SetFormDisabled, SetFormEnabled, UpdateFormErrors, UpdateFormStatus } from '@ngxs/form-plugin';
import { Action, Selector, State, Store } from '@ngxs/store';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { SocialMediaAccount } from '../../shared/enums/social-media-account';
import { DEFAULT_FORM_STATE } from '../../shared/states/base.form.state';
import { AuthActions, LoginPageActions } from '../actions';
import { Credentials } from '../models/credentials.model';
import { AuthenticationService } from '../services/authentication.service';
import { AuthState } from './auth.state';


@State({
  name: 'login',
  defaults: DEFAULT_FORM_STATE,
})
export class LoginFormState {
  /**
   * WARNING! IT CAN BLOCK LOGIN FUNCTIONALITY WITHOUT IMPLEMENTATION ON BACKEND.
   * Formating credentials for sending valid data to server (ONE33T-734)
   * @param  {Credentials} credentials
   * @returns Credentials
   */
  static getFormatedCredentials(credentials): Credentials {
    return {
      ...credentials,
      email: credentials.email.toLowerCase()
    };
  }

  @Selector()
  static pending(state: any) {
    return state.form.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.form.errors;
  }

  constructor(private navigationService: NavigationService,
              private authService: AuthenticationService,
              private store: Store) {
  }

  @Action(LoginPageActions.Login)
  login(ctx, {credentials}: LoginPageActions.Login) {
    ctx.dispatch(new SetFormDisabled('login.form'));
    ctx.dispatch(new UpdateFormStatus({status: 'pending', path: 'login.form'}));
    ctx.dispatch(new AuthActions.Login(LoginFormState.getFormatedCredentials(credentials)))
      .subscribe(
        _ => {
          const state = ctx.getState;
          const isCompanyUser = this.store.selectSnapshot(AuthState.isCompanyUser);
          const {company} = this.store.selectSnapshot(AuthState.user);

          ctx.setState({
            ...state,
            ...DEFAULT_FORM_STATE,
          });
          ctx.dispatch(new CoreActions.SnackbarOpen({message: 'Successfully logged in!'}));
          if (company && company.is_trial_available) {
            return this.navigationService.goToTrialPage();
          }
          return this.navigationService.goToHomePage(isCompanyUser);
        },
        httpError => {
          return this.handleLoginError(ctx, httpError);
        },
      );
  }

  @Action(LoginPageActions.LoginWithSocialAccount)
  loginWithSocialAccount(ctx, {token, accountType}: LoginPageActions.LoginWithSocialAccount) {
    let socialLoginAction: any;
    ctx.dispatch(new SetFormDisabled('login.form'));
    ctx.dispatch(new UpdateFormStatus({status: 'pending', path: 'login.form'}));
    (accountType === SocialMediaAccount.FACEBOOK) ? socialLoginAction = AuthActions.LoginWithFacebook.bind(this) :
      socialLoginAction = AuthActions.LoginWithGoogle.bind(this);
    ctx.dispatch(new socialLoginAction(token)).subscribe((result) => {
        const state = ctx.getState();
        ctx.setState({
          ...state,
          ...DEFAULT_FORM_STATE,
        });
        this.navigateAfterLogIn(result);
        return ctx.dispatch(new CoreActions.SnackbarOpen({message: `Successfully logged in with ${accountType}!`}));
      },
      httpError => {
        return this.handleLoginError(ctx, httpError);
      },
    );
  }

  private navigateAfterLogIn(result) {
    if (result.auth.user.company && result.auth.user.company.is_trial_available) {
      return this.navigationService.goToTrialPage();
    } else if (this.store.selectSnapshot(AuthState.isSetPasswordRequired)) {
      return this.navigationService.goToSetPasswordPage();
    } else {
      return this.navigationService.goToHomePage();
    }
  }

  private handleLoginError(ctx, httpError) {
    ctx.dispatch(new UpdateFormErrors({errors: httpError.error, path: 'login.form'}));
    ctx.dispatch(new UpdateFormStatus({status: 'invalid', path: 'login.form'}));
    return ctx.dispatch(new SetFormEnabled('login.form'));
  }
}
