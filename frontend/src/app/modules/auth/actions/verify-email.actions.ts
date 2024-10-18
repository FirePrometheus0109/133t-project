export enum VerifyEmailActionTypes {
  VerifyEmail = '[VerifyEmailComponent] VerifyEmail',
  VerifyEmailResult = '[VerifyEmailComponent] VerifyEmailResult',
}

export class VerifyEmail {
  static readonly type = VerifyEmailActionTypes.VerifyEmail;

  constructor(public token: string) {
  }
}

export class VerifyEmailResult {
  static readonly type = VerifyEmailActionTypes.VerifyEmailResult;

  constructor(public result: object) {
  }
}

export type VerifyEmailActionsUnion =
  | VerifyEmail
  | VerifyEmailResult;
