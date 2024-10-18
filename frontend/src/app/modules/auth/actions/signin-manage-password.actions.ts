import {RestoreCredentials} from '../models/credentials.model';

export enum SigninManagePasswordActionTypes {
  RestoreAccount = '[Signin Manage Password] RestoreAccount',
  SetParams = '[Signin Manage Password] SetParams',
  SetInvitationMode = '[Signin Manage Password] SetInvitationMode',
  SetPasswordForInvitedUser = '[Signin Manage Password] SetPasswordForInvitedUser',
}

export class RestoreAccount {
  static readonly type = SigninManagePasswordActionTypes.RestoreAccount;

  constructor(public restoreData: RestoreCredentials) {
  }
}

export class SetParams {
  static readonly type = SigninManagePasswordActionTypes.SetParams;

  constructor(public params: RestoreCredentials) {
  }
}

export class SetPasswordForInvitedUser {
  static readonly type = SigninManagePasswordActionTypes.SetPasswordForInvitedUser;

  constructor(public params: RestoreCredentials) {
  }
}

export class SetInvitationMode {
  static readonly type = SigninManagePasswordActionTypes.SetInvitationMode;

  constructor(public value: boolean) {
  }
}

export type SigninManagePasswordActionsUnion =
  | SetPasswordForInvitedUser
  | SetInvitationMode
  | SetParams
  | RestoreAccount;
