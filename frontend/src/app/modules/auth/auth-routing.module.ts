import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthRoute } from '../shared/constants/routes/auth-routes';
import { AccountPageComponent } from './containers/account-page.component';
import { CompanySignupPageComponent } from './containers/company-signup-page.component';
import { ForgotPasswordPageComponent } from './containers/forgot-password-page/forgot-password-page.component';
import { JobSeekerSignupPageComponent } from './containers/jobseeker-signup-page.component';
import { LoginPageComponent } from './containers/login-page.component';
import { ResetUserPasswordComponent } from './containers/reset-user-password/reset-user-password.component';
import { SigninManagePasswordComponent } from './containers/signin-manage-password.component';
import { TechnicalInfoComponent } from './containers/technical-info-page.container';
import { VerifyEmailComponent } from './containers/verify-email.component';
import { VersionInfoComponent } from './containers/version-info-page.container';
import { AccountPageResolver } from './resolvers/account-page.resolver';
import { InvitedCompanySignupResolver } from './resolvers/invited-company-signup.resolver';
import { AuthGuard } from './services/auth-guard.service';
import { LoginGuardService } from './services/login-guard.service';
import { TechnicalInfoGuard } from './services/technical-info-guard.service';

const routes: Routes = [
  {
    path: AuthRoute.loginRoute,
    component: LoginPageComponent,
    canActivate: [LoginGuardService]
  },
  {
    path: AuthRoute.forgotPassword,
    component: ForgotPasswordPageComponent,
    canActivate: [LoginGuardService]
  },
  {
    path: AuthRoute.jobSeekerSignupRoute,
    component: JobSeekerSignupPageComponent,
    canActivate: [LoginGuardService]
  },
  {
    path: AuthRoute.companySignupRoute,
    component: CompanySignupPageComponent,
    canActivate: [LoginGuardService]
  },
  {path: AuthRoute.verifyEmailRoute, component: VerifyEmailComponent},
  {path: AuthRoute.restoreAccountRoute, component: SigninManagePasswordComponent},
  {path: AuthRoute.resetPasswordRoute, component: ResetUserPasswordComponent},
  {path: AuthRoute.setPasswordForSocialLoginRoute, component: ResetUserPasswordComponent},
  {
    path: AuthRoute.invitedCompanySignupRoute,
    component: SigninManagePasswordComponent,
    resolve: {data: InvitedCompanySignupResolver}
  },
  {
    path: AuthRoute.accountRoute,
    component: AccountPageComponent,
    resolve: {userData: AccountPageResolver},
  },
  {
    path: AuthRoute.technicalInfo,
    component: TechnicalInfoComponent,
    canActivate: [AuthGuard, TechnicalInfoGuard],
  },
  {
    path: AuthRoute.versionInfo,
    component: VersionInfoComponent,
    canActivate: [AuthGuard, TechnicalInfoGuard],
  },
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AuthRoutingModule {
}
