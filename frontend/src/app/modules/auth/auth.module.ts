// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { NgxsModule } from '@ngxs/store';
import { SocialLoginModule } from 'angularx-social-login';
import { MaterialModule } from '../material';
import { SharedModule } from '../shared';
import { AuthRoutingModule } from './auth-routing.module';

// Components
import { CompanySignupComponent } from './components/company-signup-form.component';
import { EditAccountPasswordFormComponent } from './components/edit-account-password-form.component';
import { EditAccountComponent } from './components/edit-account.component';
import { ForgotPasswordFormComponent } from './components/forgot-password-form/forgot-password-form.component';
import { JobSeekerSignupComponent } from './components/job-seeker-signup-form.component';
import { LoginFormComponent } from './components/login-form.component';
import { ViewAccountComponent } from './components/view-account.component';
import { AccountPageComponent } from './containers/account-page.component';
import { CompanySignupPageComponent } from './containers/company-signup-page.component';
import { ForgotPasswordPageComponent } from './containers/forgot-password-page/forgot-password-page.component';
import { JobSeekerSignupPageComponent } from './containers/jobseeker-signup-page.component';
import { LoginPageComponent } from './containers/login-page.component';
import { ResetUserPasswordComponent } from './containers/reset-user-password/reset-user-password.component';
import { SigninManagePasswordComponent } from './containers/signin-manage-password.component';
import { SocialAuthComponent } from './containers/social-auth/social-auth.component';
import { TechnicalInfoComponent } from './containers/technical-info-page.container';
import { VerifyEmailComponent } from './containers/verify-email.component';
import { VersionInfoComponent } from './containers/version-info-page.container';

// Resolvers
import { AccountPageResolver } from './resolvers/account-page.resolver';
import { InvitedCompanySignupResolver } from './resolvers/invited-company-signup.resolver';

// Services
import { JWTTokenInterceptorProvider } from './services/auth.interceptor';

// States
import { AccountPageState } from './states/account-page.state';
import { AuthState } from './states/auth.state';
import { CompanySignupFormState } from './states/company-signup-page.state';
import { JobSeekerSignupFormState } from './states/js-signup-page.state';
import { LoginFormState } from './states/login-page.state';
import { ResetUserPasswordState } from './states/reset-user-password.state';
import { SettingsPageState } from './states/settings-page.state';
import { SigninManagePasswordState } from './states/signin-manage-password.state';
import { VerifyEmailState } from './states/verify-email.state';

export const AUTH_COMPONENTS = [
  LoginPageComponent,
  LoginFormComponent,
  JobSeekerSignupPageComponent,
  JobSeekerSignupComponent,
  CompanySignupPageComponent,
  CompanySignupComponent,
  VerifyEmailComponent,
  AccountPageComponent,
  ViewAccountComponent,
  EditAccountComponent,
  EditAccountPasswordFormComponent,
  SigninManagePasswordComponent,
  TechnicalInfoComponent,
  VersionInfoComponent,
  ForgotPasswordPageComponent,
  ForgotPasswordFormComponent,
  ResetUserPasswordComponent,
  SocialAuthComponent
];


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MaterialModule,
    SharedModule,
    AuthRoutingModule,
    SocialLoginModule,
    NgxsModule.forFeature([
      AuthState,
      LoginFormState,
      JobSeekerSignupFormState,
      CompanySignupFormState,
      VerifyEmailState,
      AccountPageState,
      SettingsPageState,
      SigninManagePasswordState,
      ResetUserPasswordState
    ]),
  ],
  declarations: AUTH_COMPONENTS,
  exports: AUTH_COMPONENTS,
  entryComponents: [
    EditAccountPasswordFormComponent,
  ],
  providers: [
    JWTTokenInterceptorProvider,
    AccountPageResolver,
    InvitedCompanySignupResolver,
  ],
})
export class AuthModule {
}
