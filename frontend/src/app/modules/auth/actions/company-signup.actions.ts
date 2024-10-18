import { SignupCredentials, SignupCredentialsMaker, SignupCredentialsRaw } from '../models/credentials.model';


export enum CompanySignupPageActionTypes {
  Signup = '[CompanySignup Page] Signup',
}


export class Signup {
  static readonly type = CompanySignupPageActionTypes.Signup;
  public credentials: SignupCredentials;

  constructor(public credentialsRaw: SignupCredentialsRaw) {
    this.credentials = SignupCredentialsMaker.create(credentialsRaw);
  }
}


export type CompanySignupPageActionsUnion =
  | Signup;
