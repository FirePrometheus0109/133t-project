export enum ViewJobDetailsJSPageActionsTypes {
  LoadJobData = '[Job Page Details] LoadJobData',
  LoadPublicJobData = '[Job Page Details] LoadPublicJobData',
  ApplyForJob = '[Job Page Details] ApplyForJob',
}

export class LoadJobData {
  static readonly type = ViewJobDetailsJSPageActionsTypes.LoadJobData;

  constructor(public jobId: number) {
  }
}

export class ApplyForJob {
  static readonly type = ViewJobDetailsJSPageActionsTypes.ApplyForJob;

  constructor(public jobId: number) {
  }
}

export class LoadPublicJobData {
  static readonly type = ViewJobDetailsJSPageActionsTypes.LoadPublicJobData;

  constructor(public jobUid: string) {
  }
}

export type ViewJobDetailsJSPageActionsUnion =
  | ApplyForJob
  | LoadJobData;
