export enum JobPageEditActionTypes {
  LoadInitialData = '[Job Page] LoadInitialData',
  UpdateJob = '[Job Page] UpdateJob',
  PreviewJob = '[Job Page] PreviewJob',
}

export class LoadInitialData {
  static readonly type = JobPageEditActionTypes.LoadInitialData;

  constructor(public id: number) {
  }
}

export class UpdateJob {
  static readonly type = JobPageEditActionTypes.UpdateJob;

  constructor(public id: number, public data: any) {
  }
}

export class PreviewJob {
  static readonly type = JobPageEditActionTypes.PreviewJob;

  constructor() {
  }
}

export type JobPageEditActionsUnion =
  | LoadInitialData
  | UpdateJob
  | PreviewJob;
