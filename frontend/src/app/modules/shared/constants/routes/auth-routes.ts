import { BaseRoute } from './base-routes';


export class AuthRoute extends BaseRoute {
  public static readonly loginRoute = 'login';
  public static readonly logoutRoute = 'logout';
  public static readonly forgotPassword = 'forgot-password';
  public static readonly jobSeekerSignupRoute = 'job-seeker-signup';
  public static readonly companySignupRoute = 'company-signup';
  public static readonly verifyEmailRoute = `verify-email/${BaseRoute.token}`;
  public static readonly restoreAccountRoute = `restore-account/${BaseRoute.user}/${BaseRoute.token}`;
  public static readonly resetPasswordRoute = `reset-password/${BaseRoute.uid}/${BaseRoute.token}`;
  public static readonly setPasswordForSocialLoginRoute = `set-password`;
  public static readonly accountRoute = 'account';
  public static readonly technicalInfo = 'technical-info';
  public static readonly versionInfo = 'version-info';
  public static readonly invitedSignupRoute = `sign-up`;
  public static readonly invitedCompanySignupRoute = `${AuthRoute.invitedSignupRoute}/${BaseRoute.user}/${BaseRoute.token}`;
}
