import {Photo} from '../../shared/models';

export enum CompanyProfilePageActionTypes {
  LoadInitialData = '[Company Profile Page] LoadInitialData',
  LoadPublicInitialData = '[Company Profile Page] LoadPublicInitialData',
  PartialUpdate = '[Company Profile Page] PartialUpdate',
  UpdateLogo = '[Company Profile Page] UpdateLogo',
  LoadJobsData = '[Company Profile Page] LoadJobsData',
  LoadPublicJobsData = '[Company Profile Page] LoadPublicJobsData',
}

export class LoadInitialData {
  static readonly type = CompanyProfilePageActionTypes.LoadInitialData;

  constructor(public id: number) {
  }
}

export class LoadPublicInitialData {
  static readonly type = CompanyProfilePageActionTypes.LoadPublicInitialData;

  constructor(public id: number) {
  }
}

export class PartialUpdate {
  static readonly type = CompanyProfilePageActionTypes.PartialUpdate;

  constructor(public part: string, public id: number, public data: any) {
  }
}

export class UpdateLogo {
  static readonly type = CompanyProfilePageActionTypes.UpdateLogo;

  constructor(public id: number, public data: Photo) {
  }
}

export class LoadJobsData {
  static readonly type = CompanyProfilePageActionTypes.LoadJobsData;

  constructor(public id: number) {
  }
}

export class LoadPublicJobsData {
  static readonly type = CompanyProfilePageActionTypes.LoadPublicJobsData;

  constructor(public id: number) {
  }
}

export type CompanyProfilePageActionsUnion =
  | LoadPublicJobsData
  | LoadJobsData
  | LoadInitialData
  | LoadPublicInitialData
  | PartialUpdate
  | UpdateLogo;
