import { SignupCredentials, SignupCredentialsMaker, SignupCredentialsRaw } from '../models/credentials.model';


export enum JobSeekerSignupPageActionTypes {
  Signup = '[JobSeekerSignup Page] Signup',
}


export class Signup {
  static readonly type = JobSeekerSignupPageActionTypes.Signup;
  public credentials: SignupCredentials;

  constructor(public credentialsRaw: SignupCredentialsRaw) {
    this.credentials = SignupCredentialsMaker.create(credentialsRaw);
  }
}


export type JobSeekerSignupPageActionsUnion =
  | Signup;
