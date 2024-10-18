export interface Credentials {
  email: string;
  password: string;
}


export interface PasswordsCredentials {
  password1: string;
  password2: string;
}


export interface SignupCredentialsRaw {
  email: string;
  passwords?: PasswordsCredentials;
  first_name: string;
  last_name: string;
  company_name?: string;
}


export interface SignupCredentials {
  email: string;
  password1: string;
  password2: string;
  first_name: string;
  last_name: string;
  company_name?: string;
}


export class SignupCredentialsMaker {
  static create(sc: SignupCredentialsRaw): SignupCredentials {
    return {
      email: sc.email,
      password1: sc.passwords.password1,
      password2: sc.passwords.password2,
      first_name: sc.first_name,
      last_name: sc.last_name,
      company_name: sc.company_name,
    };
  }
}


export interface UpdatePasswordCredentials {
  old_password: string;
  new_password1: string;
}


export interface DeleteAccountReason {
  text: string;
}


export interface RestorePasswordCredentials {
  new_password: string;
  new_password_confirm: string;
}


export interface RestoreCredentials {
  user?: number;
  uid?: string;
  token: string;
  new_password?: string;
  new_password_confirm?: string;
}
