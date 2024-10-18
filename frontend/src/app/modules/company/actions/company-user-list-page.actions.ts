export enum CompanyUserListPageActionTypes {
  LoadCompanyUsersData = '[Company Users Page] LoadCompanyUsersData',
  ChangePagination = '[Company Users Page] ChangePagination',
  DeleteCompanyUser = '[Company Users Page] DeleteCompanyUser',
}

export class LoadCompanyUsersData {
  static readonly type = CompanyUserListPageActionTypes.LoadCompanyUsersData;

  constructor(public params?: object, public limit?: number, public offset?: number) {
  }
}

export class ChangePagination {
  static readonly type = CompanyUserListPageActionTypes.ChangePagination;

  constructor(public params?: object, public limit?: number, public offset?: number) {
  }
}

export class DeleteCompanyUser {
  static readonly type = CompanyUserListPageActionTypes.DeleteCompanyUser;

  constructor(public companyUserId: number) {
  }
}

export type CompanyUserListPageActionUnion =
  | DeleteCompanyUser
  | ChangePagination
  | LoadCompanyUsersData;
