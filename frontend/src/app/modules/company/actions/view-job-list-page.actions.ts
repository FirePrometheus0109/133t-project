export enum ViewJobListPageActionTypes {
  LoadJobsData = '[View Job Page] LoadJobData',
  ChangeGrid = '[View Job Page] ChangeGrid',
  DeleteJob = '[View Job Page] DeleteJob',
  DeleteJobList = '[View Job Page] DeleteJobList',
  RestoreJob = '[View Job Page] RestoreJob',
  DownloadJobList = '[View Job Page] DownloadJobList',
  UpdateParams = '[View Job Page] UpdateParams',
  RemoveParams = '[View Job Page] RemoveParams',
  LoadJobsAuthorsData = '[View Job Page] LoadJobAuthorsData'
}

export class LoadJobsData {
  static readonly type = ViewJobListPageActionTypes.LoadJobsData;

  constructor(public params?: object, public limit?: number, public offset?: number) {
  }
}

export class ChangeGrid {
  static readonly type = ViewJobListPageActionTypes.ChangeGrid;

  constructor(public params?: object, public limit?: number, public offset?: number) {
  }
}

export class DeleteJob {
  static readonly type = ViewJobListPageActionTypes.DeleteJob;

  constructor(public jobId: number) {
  }
}

export class DeleteJobList {
  static readonly type = ViewJobListPageActionTypes.DeleteJobList;

  constructor(public jobIds: number[]) {
  }
}

export class DownloadJobList {
  static readonly type = ViewJobListPageActionTypes.DownloadJobList;

  constructor(public jobIds: number[]) {
  }
}

export class RestoreJob {
  static readonly type = ViewJobListPageActionTypes.RestoreJob;

  constructor(public jobId: number, public data?: object) {
  }
}


export class UpdateParams {
  static readonly type = ViewJobListPageActionTypes.UpdateParams;

  constructor(public params: any, public changeType: string) {
  }
}


export class RemoveParams {
  static readonly type = ViewJobListPageActionTypes.RemoveParams;

  constructor(public paramsToDelete: string[]) {
  }
}


export class LoadJobsAuthorsData {
  static readonly type = ViewJobListPageActionTypes.LoadJobsAuthorsData;

  constructor() {
  }
}

export type ViewJobListPageActionUnion =
  | RemoveParams
  | UpdateParams
  | DownloadJobList
  | LoadJobsData
  | ChangeGrid
  | DeleteJob
  | DeleteJobList
  | RestoreJob
  | LoadJobsAuthorsData;
