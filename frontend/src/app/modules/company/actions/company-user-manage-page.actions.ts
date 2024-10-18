import {GroupedPermission} from '../../shared/models/permissions.model';
import {CompanyUserData} from '../models/company-user.model';

export enum CompanyUserManageActionsTypes {
  LoadGroupedPermissions = '[Manage Company User] LoadGroupedPermissions',
  SetInviteMode = '[Manage Company User] SetInviteMode',
  SetEditMode = '[Manage Company User] SetEditMode',
  SetViewMode = '[Manage Company User] SetViewMode',
  SetSelectedPermissions = '[Manage Company User] SetSelectedPermissions',
  InviteCompanyUser = '[Manage Company User] InviteCompanyUser',
  LoadCompanyUserData = '[Manage Company User] LoadCompanyUserData',
  ResetCurrentCompanyUser = '[Manage Company User] ResetCurrentCompanyUser',
  SaveCompanyUser = '[Manage Company User] SaveCompanyUser',
  RestoreDeletedCompanyUser = '[Manage Company User] RestoreDeletedCompanyUser',
  LoadInitialGroupedPermissions = '[Manage Company User] LoadInitialGroupedPermissions',
}

export class LoadGroupedPermissions {
  static readonly type = CompanyUserManageActionsTypes.LoadGroupedPermissions;
}

export class LoadInitialGroupedPermissions {
  static readonly type = CompanyUserManageActionsTypes.LoadInitialGroupedPermissions;
}

export class SetInviteMode {
  static readonly type = CompanyUserManageActionsTypes.SetInviteMode;

  constructor(public value: boolean) {
  }
}

export class SetEditMode {
  static readonly type = CompanyUserManageActionsTypes.SetEditMode;

  constructor(public value: boolean) {
  }
}

export class SetViewMode {
  static readonly type = CompanyUserManageActionsTypes.SetViewMode;

  constructor(public value: boolean) {
  }
}

export class SetSelectedPermissions {
  static readonly type = CompanyUserManageActionsTypes.SetSelectedPermissions;

  constructor(public selectedPermission: GroupedPermission) {
  }
}

export class InviteCompanyUser {
  static readonly type = CompanyUserManageActionsTypes.InviteCompanyUser;

  constructor(public userData: CompanyUserData) {
  }
}

export class LoadCompanyUserData {
  static readonly type = CompanyUserManageActionsTypes.LoadCompanyUserData;

  constructor(public userId: number) {
  }
}

export class ResetCurrentCompanyUser {
  static readonly type = CompanyUserManageActionsTypes.ResetCurrentCompanyUser;
}

export class SaveCompanyUser {
  static readonly type = CompanyUserManageActionsTypes.SaveCompanyUser;

  constructor(public userId: number, public userData: CompanyUserData) {
  }
}

export class RestoreDeletedCompanyUser {
  static readonly type = CompanyUserManageActionsTypes.RestoreDeletedCompanyUser;

  constructor(public userData: CompanyUserData) {
  }
}

export type CompanyUserManageActionsUnion =
  | LoadInitialGroupedPermissions
  | RestoreDeletedCompanyUser
  | SaveCompanyUser
  | ResetCurrentCompanyUser
  | LoadCompanyUserData
  | InviteCompanyUser
  | SetSelectedPermissions
  | LoadGroupedPermissions
  | SetInviteMode
  | SetEditMode
  | SetViewMode;
