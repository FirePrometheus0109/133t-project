export enum JobSeekerDashboardTypes {
  LoadInitialData = '[Job Seeker Dashboard] LoadInitialData',
  GetLastViewsList = '[Job Seeker Dashboard] GetLastViewsList',
  SetCurrentPagination = '[Job Seeker Dashboard] SetCurrentPagination',
  GetAutoApplyProgress = '[Job Seeker Dashboard] GetAutoApplyProgress',
}


export class LoadInitialData {
  static readonly type = JobSeekerDashboardTypes.LoadInitialData;

  constructor(public jsId: number) {
  }
}


export class GetLastViewsList {
  static readonly type = JobSeekerDashboardTypes.GetLastViewsList;

  constructor(public jsId: number, public params?: object) {
  }
}


export class SetCurrentPagination {
  static readonly type = JobSeekerDashboardTypes.SetCurrentPagination;

  constructor(public params: object) {
  }
}


export class GetAutoApplyProgress {
  static readonly type = JobSeekerDashboardTypes.GetAutoApplyProgress;
}


export type JobSeekerDashboardActionUnions =
  | GetAutoApplyProgress
  | SetCurrentPagination
  | GetLastViewsList
  | LoadInitialData;
