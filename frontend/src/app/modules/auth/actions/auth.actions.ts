import { SubscriptionModel, SubscriptionPlan } from '../../subscription/models/subsctiption-plan.model';
import { Credentials, SignupCredentials } from '../models/credentials.model';


export enum AuthActionTypes {
  Initial = '[Auth] Initial',
  Login = '[Auth] Login',
  VerifyToken = '[Auth] VerifyToken',
  RefreshToken = '[Auth] RefreshToken',
  ExtractTokenExpirationDate = '[Auth] ExtractTokenExpirationDate',
  SetLockOnRefresh = '[Auth] SetLockOnRefresh',
  JobSeekerSignup = '[Auth] JobSeekerSignup',
  CompanySignup = '[Auth] CompanySignup',
  VerifyEmail = '[Auth] VerifyEmail',
  Logout = '[Auth] Logout',
  CleanAuthData = '[Auth] CleanAuthData',
  ReloadUserPermissions = '[Auth] ReloadUserPermissions',
  ReloadAllPermissions = '[Auth] ReloadAllPermissions',
  UpdateBillingInformation = '[Auth] UpdateBillingInformation',
  LoginWithFacebook = '[Auth] LoginWithFacebook',
  LoginWithGoogle = '[Auth] LoginWithGoogle',
  UpdateSubsctiption = '[Auth] UpdateSubsctiption '
}


export class Initial {
  static readonly type = AuthActionTypes.Initial;
}


export class Login {
  static readonly type = AuthActionTypes.Login;

  constructor(public credentials: Credentials) {
  }
}


export class LoginWithFacebook {
  static readonly type = AuthActionTypes.LoginWithFacebook;

  constructor(public authToken) {
  }
}


export class LoginWithGoogle {
  static readonly type = AuthActionTypes.LoginWithGoogle;

  constructor(public authToken) {
  }
}


export class VerifyToken {
  static readonly type = AuthActionTypes.VerifyToken;

  constructor(public existsToken: string) {
  }
}

export class SetLockOnRefresh {
  static readonly type = AuthActionTypes.SetLockOnRefresh;

  constructor(public isLocked: boolean = true) {
  }
}

export class ExtractTokenExpirationDate {
  static readonly type = AuthActionTypes.ExtractTokenExpirationDate;
}

export class RefreshToken {
  static readonly type = AuthActionTypes.RefreshToken;

  constructor(public existsToken: string) {
  }
}


export class JobSeekerSignup {
  static readonly type = AuthActionTypes.JobSeekerSignup;

  constructor(public credentials: SignupCredentials) {
  }
}


export class CompanySignup {
  static readonly type = AuthActionTypes.CompanySignup;

  constructor(public credentials: SignupCredentials) {
  }
}


export class VerifyEmail {
  static readonly type = AuthActionTypes.VerifyEmail;

  constructor(public token: string) {
  }
}


export class Logout {
  static readonly type = AuthActionTypes.Logout;
}


export class CleanAuthData {
  static readonly type = AuthActionTypes.CleanAuthData;
}


export class UpdateBillingInformation {
  static readonly type = AuthActionTypes.UpdateBillingInformation;
}


export class ReloadUserPermissions {
  static readonly type = AuthActionTypes.ReloadUserPermissions;
}


export class ReloadAllPermissions {
  static readonly type = AuthActionTypes.ReloadAllPermissions;
}

export class UpdateSubsctiption {
  static readonly type = AuthActionTypes.UpdateSubsctiption;

  constructor(public plan: SubscriptionModel) {
  }
}

export type AuthActionsUnion =
  | LoginWithFacebook
  | LoginWithGoogle
  | Initial
  | Login
  | VerifyToken
  | RefreshToken
  | SetLockOnRefresh
  | ExtractTokenExpirationDate
  | JobSeekerSignup
  | CompanySignup
  | VerifyEmail
  | Logout
  | CleanAuthData
  | ReloadUserPermissions
  | ReloadAllPermissions
  | UpdateBillingInformation
  | UpdateSubsctiption;
