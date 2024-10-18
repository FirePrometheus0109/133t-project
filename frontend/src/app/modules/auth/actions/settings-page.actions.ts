import {DeleteAccountReason} from '../models/credentials.model';

export enum SettingsPageActionsTypes {
  DeleteAccount = '[Settings] DeleteAccount',
}

export class DeleteAccount {
  static readonly type = SettingsPageActionsTypes.DeleteAccount;

  constructor(public deletionReason: DeleteAccountReason) {
  }
}

export type SettingsPageActionsUnion =
  | DeleteAccount;
