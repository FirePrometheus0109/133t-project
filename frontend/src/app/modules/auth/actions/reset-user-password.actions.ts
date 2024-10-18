import { RestoreCredentials, RestorePasswordCredentials } from '../models/credentials.model';


export enum ResetUserPasswordPageActionTypes {
  SetTemporaryEmailField = '[Reset User Password] SetTemporaryEmailField',
  SendForgotPassword = '[Reset User Password] SendForgotPassword',
  ConfirmResetPassword = '[Reset User Password] ConfirmResetPassword',
  SetPassword = '[Reset User Password] SetPassword',
}


export class SetTemporaryEmailField {
  static readonly type = ResetUserPasswordPageActionTypes.SetTemporaryEmailField;

  constructor(public email: string) {
  }
}


export class SendForgotPassword {
  static readonly type = ResetUserPasswordPageActionTypes.SendForgotPassword;

  constructor(public email: object) {
  }
}


export class ConfirmResetPassword {
  static readonly type = ResetUserPasswordPageActionTypes.ConfirmResetPassword;

  constructor(public params: RestoreCredentials) {
  }
}


export class SetPassword {
  static readonly type = ResetUserPasswordPageActionTypes.SetPassword;

  constructor(public passwords: RestorePasswordCredentials) {
  }
}


export type ResetUserPasswordPageActionsUnion =
  | SetPassword
  | ConfirmResetPassword
  | SendForgotPassword
  | SetTemporaryEmailField;
