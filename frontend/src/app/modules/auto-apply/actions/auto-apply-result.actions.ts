import {CoverLetterApplyData} from '../../shared/models/cover-letter.model';

export enum AutoApplyResultActionsTypes {
  LoadAutoApply = '[Auto Apply Result] LoadAutoApply',
  GetSelectedJob = '[Auto Apply Result] GetSelectedJob',
  GetAutoApplyResult = '[Auto Apply Result] GetAutoApplyResult',
  StopAutoApply = '[Auto Apply Result] StopAutoApply',
  RestartAutoApply = '[Auto Apply Result] RestartAutoApply',
  ApplyForNewJob = '[Auto Apply Result] ApplyForNewJob',
  SetCoverLetterForApply = '[Auto Apply Result] SetCoverLetterForApply',
}

export class LoadAutoApply {
  static readonly type = AutoApplyResultActionsTypes.LoadAutoApply;

  constructor(public autoApplyId: number) {
  }
}

export class GetAutoApplyResult {
  static readonly type = AutoApplyResultActionsTypes.GetAutoApplyResult;

  constructor(public autoApplyId: number) {
  }
}

export class StopAutoApply {
  static readonly type = AutoApplyResultActionsTypes.StopAutoApply;

  constructor(public autoApplyId: number) {
  }
}

export class RestartAutoApply {
  static readonly type = AutoApplyResultActionsTypes.RestartAutoApply;

  constructor(public autoApplyId: number) {
  }
}

export class ApplyForNewJob {
  static readonly type = AutoApplyResultActionsTypes.ApplyForNewJob;

  constructor(public autoApplyId: number, public jobId: number) {
  }
}

export class GetSelectedJob {
  static readonly type = AutoApplyResultActionsTypes.GetSelectedJob;

  constructor(public jobId: number) {
  }
}

export class SetCoverLetterForApply {
  static readonly type = AutoApplyResultActionsTypes.SetCoverLetterForApply;

  constructor(public autoApplyId: number, public jobId: number, public coverLetterData: CoverLetterApplyData) {
  }
}

export type AutoApplyResultActionsUnion =
  | SetCoverLetterForApply
  | ApplyForNewJob
  | RestartAutoApply
  | StopAutoApply
  | GetAutoApplyResult
  | LoadAutoApply
  | GetSelectedJob;
