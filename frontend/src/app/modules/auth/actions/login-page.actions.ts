import { Credentials } from '../models/credentials.model';


export enum LoginPageActionTypes {
  Login = '[Login Page] Login',
  LoginWithSocialAccount = '[Login Page] LoginWithSocialAccount',
}


export class Login {
  static readonly type = LoginPageActionTypes.Login;

  constructor(public credentials: Credentials) {
  }
}


export class LoginWithSocialAccount {
  static readonly type = LoginPageActionTypes.LoginWithSocialAccount;

  constructor(public token: string, public accountType: string) {
  }
}


export type LoginPageActionsUnion =
  | LoginWithSocialAccount
  | Login;
