import { Action, Selector, State, StateContext } from '@ngxs/store';
import { NgxPermissionsService } from 'ngx-permissions';
import { of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { environment } from '../../../../environments/environment';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { DateTimeHelper } from '../../shared/helpers/date-time.helper';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { UtilsService } from '../../shared/services/utils.service';
import { AuthActions, VerifyEmailActions } from '../actions';
import { LoggedUser, Permission } from '../models/user.model';
import { AuthenticationService } from '../services';

import jwt_decode from 'jwt-decode';


export class AuthStateModel {
  token?: string;
  /**
   * @property {number} expiresAt - JWT token expiration date in secconds.
   * MARK: Data() object understand data in miliseconds,
   * so to convert it we should do like this: new Date(expiresAt*1000)
   */
  expiresAt?: number;
  user?: LoggedUser;
  isAuthorized?: boolean;
  allPermissions: Array<Permission>;
  /**
   * @property {boolean} refreshingTokenLock -
   * State that describe lock from dispatching tokenRefresh action if refresh was called once and now processing.
   * It's need to switch from "check and launch token refresh" case from auth interceptor to
   * "collecting failed request by expired token to repeat after" case.
   */
  refreshingTokenLock: boolean;
  isSetPasswordRequired: boolean;
}


const DEFAULT_AUTH_STATE = {
  token: null,
  expiresAt: null,
  user: null,
  isAuthorized: false,
  allPermissions: null,
  refreshingTokenLock: false,
  isSetPasswordRequired: false
};


@State<AuthStateModel>({
  name: 'auth',
  defaults: DEFAULT_AUTH_STATE,
})
export class AuthState {

  constructor(private authService: AuthenticationService,
              private navigationService: NavigationService,
              private permissionsService: NgxPermissionsService) {
  }

  @Selector()
  static token(state: AuthStateModel): string {
    return state.token;
  }

  @Selector()
  static expiresAt(state: AuthStateModel): number {
    return state.expiresAt;
  }

  @Selector()
  static isAuthorized(state: AuthStateModel): boolean {
    return state.isAuthorized;
  }

  @Selector()
  static username(state: AuthStateModel): string {
    return state.user['username'];
  }

  @Selector()
  static user(state: AuthStateModel): LoggedUser {
    return state.user;
  }

  @Selector()
  static companyId(state: AuthStateModel) {
    return state.user.company && state.user.company.id;
  }

  @Selector()
  static isCompanyUser(state: AuthStateModel): boolean {
    return Boolean(AuthState.companyId(state));
  }

  @Selector()
  static isSubsctiptionPurchased(state: AuthStateModel): boolean {
    return state.user.company && state.user.company.subscription
      && state.user.company.subscription.hasOwnProperty('id');
  }

  @Selector()
  static isSubscriptionExpired(state: AuthStateModel): boolean {
    return state.user.company && !state.user.company.is_trial_available &&
      (UtilsService.isEmptyObject(state.user.company.subscription) ||
        state.user.company.subscription && DateTimeHelper.isDateExpired(state.user.company.subscription.date_end));
  }

  @Selector()
  static isSubscriptionDeleted(state: AuthStateModel): boolean {
    return UtilsService.isEmptyObject(state.user.company.subscription);
  }

  @Selector()
  static jobseekerId(auth) {
    return auth.user.job_seeker && auth.user.job_seeker.id;
  }

  @Selector()
  static isJobSeeker(state: AuthStateModel): boolean {
    return state.user.job_seeker && state.user.job_seeker.hasOwnProperty('id');
  }

  @Selector()
  static permissions(state: AuthStateModel): Permission[] {
    return state.user.permissions;
  }

  @Selector()
  static allPermissions(state: AuthStateModel): Permission[] {
    return state.allPermissions;
  }

  @Selector()
  static refreshingTokenLock(state: AuthStateModel): boolean {
    return state.refreshingTokenLock;
  }

  @Selector()
  static isSetPasswordRequired(state: AuthStateModel): boolean {
    return state.isSetPasswordRequired;
  }

  /**
   * Using only for process login responses.
   */
  private static loginHandler(ctx: StateContext<AuthStateModel>, user, token: string, is_password_set?: boolean) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      token: token,
      user: user,
      isSetPasswordRequired: !is_password_set,
    });
    ctx.dispatch(new AuthActions.ExtractTokenExpirationDate());
    ctx.dispatch(new CoreActions.DispatchActionsOnInit());
  }

  @Action(AuthActions.Initial)
  initial(ctx: StateContext<AuthStateModel>) {
    const state = ctx.getState();
    const isAuthorized = (state.token !== null && state.token !== undefined && state.token !== '');
    return ctx.setState({
      ...state,
      isAuthorized: isAuthorized,
    });
  }

  @Action(AuthActions.Login)
  login(ctx: StateContext<AuthStateModel>, {credentials}: AuthActions.Login) {
    return this.authService.login(credentials).pipe(
      tap(({user, token}) => {
        AuthState.loginHandler(ctx, user, token);
      }),
    );
  }

  @Action(AuthActions.LoginWithFacebook)
  loginWithFacebook(ctx: StateContext<AuthStateModel>, {authToken}: AuthActions.LoginWithFacebook) {
    return this.authService.loginWithFacebook(authToken).pipe(
      tap(({user, token}) => {
        AuthState.loginHandler(ctx, user, token, user.job_seeker.is_password_set);
      }),
    );
  }

  @Action(AuthActions.LoginWithGoogle)
  loginWithGoogle(ctx: StateContext<AuthStateModel>, {authToken}: AuthActions.LoginWithGoogle) {
    return this.authService.loginWithGoogle(authToken).pipe(
      tap(({user, token}) => {
        AuthState.loginHandler(ctx, user, token, user.job_seeker.is_password_set);
      }),
    );
  }

  @Action(AuthActions.VerifyToken)
  verifyToken(ctx: StateContext<AuthStateModel>, {existsToken}: AuthActions.VerifyToken) {
    return this.authService.verifyToken(existsToken).pipe(
      map(({token}) => {
        if (token) {
          const state = ctx.getState();
          ctx.setState({
            ...state,
            token: token,
            isAuthorized: true,
          });
          ctx.dispatch(new AuthActions.ExtractTokenExpirationDate());
          return true;
        } else {
          ctx.dispatch(new AuthActions.Logout());
          return false;
        }
      }),
    );
  }

  @Action(AuthActions.ExtractTokenExpirationDate)
  extractTokenExpirationDate(ctx: StateContext<AuthStateModel>) {
    const state = ctx.getState();
    const token = AuthState.token(state);
    if (token) {
      const {exp} = jwt_decode(token);
      return ctx.setState({
        ...state,
        expiresAt: exp
      });
    }
  }

  @Action(AuthActions.SetLockOnRefresh)
  setLockOnRefresh(ctx: StateContext<AuthStateModel>, {isLocked}: AuthActions.SetLockOnRefresh) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      refreshingTokenLock: isLocked
    });
  }

  @Action(AuthActions.RefreshToken)
  refreshToken(ctx: StateContext<AuthStateModel>, {existsToken}: AuthActions.RefreshToken) {
    const state = ctx.getState();

    ctx.dispatch(new AuthActions.SetLockOnRefresh(true));

    return this.authService.refreshToken(existsToken)
      .pipe(
        tap(({token}) => {
          if (token) {
            ctx.setState({
              ...state,
              token: token,
              isAuthorized: true
            });
          }
          ctx.dispatch(new AuthActions.ExtractTokenExpirationDate());
          ctx.dispatch(new AuthActions.SetLockOnRefresh(false));
        }),
        catchError(error => {
          return of(error);
        })
      );
  }

  @Action(AuthActions.JobSeekerSignup)
  jobSeekerSignup(ctx: StateContext<AuthStateModel>, {credentials}: AuthActions.JobSeekerSignup) {
    return this.authService.jobSeekerSignup(credentials).pipe(
      tap(result => {
        return this.handleSuccessSnackBar(ctx, result);
      }),
    );
  }

  @Action(AuthActions.CompanySignup)
  companySignup(ctx: StateContext<AuthStateModel>, {credentials}: AuthActions.CompanySignup) {
    return this.authService.companySignup(credentials).pipe(
      tap(result => {
        return this.handleSuccessSnackBar(ctx, result);
      }),
    );
  }

  @Action(AuthActions.VerifyEmail)
  verifyEmail({dispatch}: StateContext<AuthStateModel>, {token}: AuthActions.VerifyEmail) {
    return this.authService.verifyEmail(token).pipe(
      tap(result => dispatch(new VerifyEmailActions.VerifyEmailResult(result))),
    );
  }

  @Action(AuthActions.Logout)
  logout(ctx: StateContext<AuthStateModel>) {
    return this.authService.logout().pipe(tap((result) => {
      this.permissionsService.flushPermissions();
      this.handleSuccessSnackBar(ctx, result);
      ctx.dispatch(new AuthActions.CleanAuthData());
      return this.navigationService.goToHomePage();
    }));
  }

  @Action(AuthActions.CleanAuthData)
  cleanAuthData(ctx: StateContext<AuthStateModel>) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      ...DEFAULT_AUTH_STATE,
    });
  }

  @Action(AuthActions.ReloadUserPermissions)
  reloadUserPermissions(ctx: StateContext<AuthStateModel>) {
    return this.authService.getUserPermissions().pipe((tap(userPermissions => {
      const state = ctx.getState();
      const user = state.user;
      user.permissions = userPermissions;
      const permissions = userPermissions.map(x => x.codename);
      this.permissionsService.loadPermissions(permissions);
      ctx.setState({
        ...state,
        user: user,
      });
    })));
  }

  @Action(AuthActions.ReloadAllPermissions)
  reloadAllPermissions(ctx: StateContext<AuthStateModel>) {
    return this.authService.getAllSystemPermissions().pipe((tap(allPermissions => {
      const state = ctx.getState();
      return ctx.setState({
        ...state,
        allPermissions: allPermissions,
      });
    })));
  }

  @Action(AuthActions.UpdateBillingInformation)
  updateBillingInformation(ctx: StateContext<AuthStateModel>) {
    const state = ctx.getState();
    const updatedUser = state.user;
    updatedUser.company.is_billing_info_provided = true;
    return ctx.setState({
      ...state,
      user: updatedUser,
    });
  }

  @Action(AuthActions.UpdateSubsctiption)
  updateSubsctiption(ctx: StateContext<AuthStateModel>, {plan}: AuthActions.UpdateSubsctiption) {
    const state = ctx.getState();
    const updatedUser = state.user;
    updatedUser.company.subscription = plan;
    return ctx.setState({
      ...state,
      user: updatedUser,
    });
  }

  private handleSuccessSnackBar(ctx: StateContext<AuthStateModel>, result: any) {
    return ctx.dispatch(new CoreActions.SnackbarOpen({
      message: result['detail'],
      delay: environment.snackBarDelay,
      type: SnackBarMessageType.SUCCESS,
    }));
  }
}
