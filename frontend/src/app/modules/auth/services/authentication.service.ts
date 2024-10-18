import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '../../shared/services/api.service';
import {
  Credentials, DeleteAccountReason, RestoreCredentials, RestorePasswordCredentials, SignupCredentials
} from '../models/credentials.model';
import { LoggedUser, Permission } from '../models/user.model';


@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  route = 'auth';
  password = 'password';
  passwordReset = 'password-reset';
  passwordResetConfirm = 'password-reset-confirm';
  deleteAccountRoute = 'delete-account';
  restoreAccountRoute = 'restore-account';
  invitedCompanyUserSignup = 'invited-company-user-sign-up';
  permissions = 'permissions';
  allPermissions = 'all-permissions';
  loginPath = 'login';
  passwordSet = 'set-password';
  google = 'google';
  facebook = 'facebook';

  constructor(private api: ApiService) {
  }

  refreshToken(token: string): Observable<any> {
    return this.api.post(`${this.route}/api-token-refresh`, {token: token});
  }

  verifyToken(token: string): Observable<any> {
    return this.api.post(`${this.route}/api-token-verify`, {token: token});
  }

  companySignup(user: SignupCredentials): Observable<any> {
    return this.api.post(`${this.route}/company-signup`, user);
  }

  jobSeekerSignup(user: SignupCredentials): Observable<any> {
    return this.api.post(`${this.route}/job-seeker-signup`, user);
  }

  login(credentials: Credentials): Observable<{user: LoggedUser; token: string}> {
    return this.api.post(`${this.route}/login`, {email: credentials.email, password: credentials.password}).pipe(
      map(result => {
        return {user: result['user'], token: result['token']};
      }));
  }

  logout(): Observable<any> {
    return this.api.post(`${this.route}/logout`);
  }

  verifyEmail(key: string): Observable<object> {
    return this.api.post(`${this.route}/verify-email`, {key: key});
  }

  getUserData(): Observable<any> {
    return this.api.get(`${this.route}/user`);
  }

  putUserData(data: {}): Observable<any> {
    return this.api.put(`${this.route}/user`, data);
  }

  updatePassword(data: {}): Observable<any> {
    return this.api.post(`${this.route}/${this.password}/change`, data);
  }

  deleteAccount(deletionReason: DeleteAccountReason): Observable<any> {
    return this.api.post(`${this.route}/${this.deleteAccountRoute}`, deletionReason);
  }

  restoreAccount(restoreData: RestoreCredentials): Observable<any> {
    return this.api.post(`${this.route}/${this.restoreAccountRoute}`, restoreData);
  }

  setInvitedUserPassword(restoreData: RestoreCredentials): Observable<any> {
    return this.api.post(`${this.route}/${this.invitedCompanyUserSignup}`, restoreData);
  }

  getUserPermissions(): Observable<Array<Permission>> {
    return this.api.get(`${this.route}/${this.permissions}`, {});
  }

  getAllSystemPermissions(): Observable<Array<Permission>> {
    return this.api.get(`${this.route}/${this.allPermissions}`, {});
  }

  sendForgotPassword(email: object): Observable<any> {
    return this.api.post(`${this.route}/${this.passwordReset}`, email);
  }

  confirmResetPassword(params: RestoreCredentials): Observable<any> {
    return this.api.post(`${this.route}/${this.passwordResetConfirm}`, params);
  }

  setPassword(passwords: RestorePasswordCredentials): Observable<any> {
    return this.api.post(`${this.route}/${this.passwordSet}`, passwords);
  }

  loginWithGoogle(token: string): Observable<any> {
    return this.api.post(`${this.route}/${this.google}/${this.loginPath}`, {access_token: token});
  }

  loginWithFacebook(token: string): Observable<any> {
    return this.api.post(`${this.route}/${this.facebook}/${this.loginPath}`, {access_token: token});
  }
}
