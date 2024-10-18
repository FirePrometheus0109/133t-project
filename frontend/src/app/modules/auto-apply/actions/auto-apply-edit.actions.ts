export enum AutoApplyEditActionsTypes {
  LoadAutoApply = '[Auto Apply Edit] LoadAutoApply',
  SetQueryParams = '[Auto Apply Edit] SetQueryParams',
  SaveAutoApply = '[Auto Apply Edit] SaveAutoApply',
  SetCreateMode = '[Auto Apply Edit] SetCreateMode',
  CreateAutoApply = '[Auto Apply Edit] CreateAutoApply',
  UpdateAutoApply = '[Auto Apply Edit] UpdateAutoApply',
  LoadAutoApplyJobsList = '[Auto Apply Edit] LoadAutoApplyJobsList',
  GetSelectedJob = '[Auto Apply Edit] GetSelectedJob',
  SetDeletedJobs = '[Auto Apply Edit] SetDeletedJobs',
  SetStoppedJobs = '[Auto Apply Edit] SetStoppedJobs',
  ReturnJobFromStopped = '[Auto Apply Edit] ReturnJobFromStopped',
  SetTitle = '[Auto Apply Edit] SetTitle',
  SetSpecifyNumber = '[Auto Apply Edit] SetSpecifyNumber',
  SetAppliedJobs = '[Auto Apply Edit] SetAppliedJobs',
  StartAutoApply = '[Auto Apply Edit] StartAutoApply',
  CleanAutoApplyData = '[Auto Apply Edit] CleanAutoApplyData',
  CreateAutoApplyFromId = '[Auto Apply Edit] CreateAutoApplyFromId',
  LoadAutoApplyJobs = '[Auto Apply Edit] LoadAutoApplyJobs',
}

export class LoadAutoApply {
  static readonly type = AutoApplyEditActionsTypes.LoadAutoApply;

  constructor(public autoApplyId: number) {
  }
}

export class SetQueryParams {
  static readonly type = AutoApplyEditActionsTypes.SetQueryParams;

  constructor(public params: any) {
  }
}

export class SetDeletedJobs {
  static readonly type = AutoApplyEditActionsTypes.SetDeletedJobs;

  constructor(public deletedJobId: number) {
  }
}

export class SetStoppedJobs {
  static readonly type = AutoApplyEditActionsTypes.SetStoppedJobs;

  constructor(public jobIdToStop: number) {
  }
}

export class ReturnJobFromStopped {
  static readonly type = AutoApplyEditActionsTypes.ReturnJobFromStopped;

  constructor(public stoppedJobId: number) {
  }
}

export class LoadAutoApplyJobsList {
  static readonly type = AutoApplyEditActionsTypes.LoadAutoApplyJobsList;

  constructor() {
  }
}

export class LoadAutoApplyJobs {
  static readonly type = AutoApplyEditActionsTypes.LoadAutoApplyJobs;

  constructor(public autoApplyId: number) {
  }
}

export class SaveAutoApply {
  static readonly type = AutoApplyEditActionsTypes.SaveAutoApply;

  constructor(public params: any) {
  }
}

export class UpdateAutoApply {
  static readonly type = AutoApplyEditActionsTypes.UpdateAutoApply;

  constructor(public params: any, public autoApplyId: number) {
  }
}

export class SetCreateMode {
  static readonly type = AutoApplyEditActionsTypes.SetCreateMode;
}

export class CreateAutoApply {
  static readonly type = AutoApplyEditActionsTypes.CreateAutoApply;

  constructor(public params: any) {
  }
}

export class GetSelectedJob {
  static readonly type = AutoApplyEditActionsTypes.GetSelectedJob;

  constructor(public jobId: number) {
  }
}

export class SetSpecifyNumber {
  static readonly type = AutoApplyEditActionsTypes.SetSpecifyNumber;

  constructor(public number: number) {
  }
}

export class SetTitle {
  static readonly type = AutoApplyEditActionsTypes.SetTitle;

  constructor(public title: string) {
  }
}

export class SetAppliedJobs {
  static readonly type = AutoApplyEditActionsTypes.SetAppliedJobs;
}

export class StartAutoApply {
  static readonly type = AutoApplyEditActionsTypes.StartAutoApply;

  constructor(public autoApplyId: number, public appliedJobs: any) {
  }
}

export class CleanAutoApplyData {
  static readonly type = AutoApplyEditActionsTypes.CleanAutoApplyData;
}

export class CreateAutoApplyFromId {
  static readonly type = AutoApplyEditActionsTypes.CreateAutoApplyFromId;

  constructor(public autoApplyId: number) {
  }
}

export type AutoApplyEditActionsUnion =
  | LoadAutoApplyJobs
  | CreateAutoApplyFromId
  | LoadAutoApply
  | LoadAutoApplyJobsList
  | SetCreateMode
  | CreateAutoApply
  | UpdateAutoApply
  | SaveAutoApply
  | GetSelectedJob
  | SetDeletedJobs
  | SetStoppedJobs
  | ReturnJobFromStopped
  | SetTitle
  | SetSpecifyNumber
  | SetAppliedJobs
  | StartAutoApply
  | SetQueryParams
  | CleanAutoApplyData;
