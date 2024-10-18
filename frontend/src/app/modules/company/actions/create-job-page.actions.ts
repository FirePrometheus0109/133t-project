export enum CreateJobPageActionTypes {
  LoadInitialData = '[Create Job Page] LoadInitialData',
  CreateNewJob = '[Create Job Page] CreateNewJob',
}

export class LoadInitialData {
  static readonly type = CreateJobPageActionTypes.LoadInitialData;
}

export class CreateNewJob {
  static readonly type = CreateJobPageActionTypes.CreateNewJob;

  constructor(public data: any, public successPostMessage: string) {
  }
}

export type CreateJobPageActionsUnion =
  | LoadInitialData
  | CreateNewJob;
