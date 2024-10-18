export enum AccountPageTypes {
  GetAccountData = '[Account] GetAccountData',
  UpdateAccountData = '[Account] UpdateAccountData',
  UpdateAccountPassword = '[Account] UpdateAccountPassword',
  ToggleEditMode = '[Account] ToggleEditMode',
}

export class GetAccountData {
  static readonly type = AccountPageTypes.GetAccountData;
}

export class UpdateAccountData {
  static readonly type = AccountPageTypes.UpdateAccountData;

  constructor(public data: {}) {
  }
}

export class UpdateAccountPassword {
  static readonly type = AccountPageTypes.UpdateAccountPassword;

  constructor(public data: {}) {
  }
}

export class ToggleEditMode {
  static readonly type = AccountPageTypes.ToggleEditMode;

  constructor(public isEdit: boolean) {
  }
}

export type AccountPageActionsUnion =
  | GetAccountData
  | UpdateAccountData
  | UpdateAccountPassword
  | ToggleEditMode;
