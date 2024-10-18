import { CoverLetterApplyData } from '../../shared/models/cover-letter.model';


export enum ManualApplyActionTypes {
  ManualApplyForJob = '[Manual Apply] ManualApplyForJob',
  ChangeManualApplyValidationMessage = '[Manual Apply] ChangeManualApplyValidationMessage',
  ChangeManualApplyPossibility = '[Manual Apply] ChangeManualApplyPossibility',
  ResetManualApplyState = '[Manual Apply] ResetManualApplyState',
  ReapplyForJob = '[Manual Apply] ReapplyForJob'
}


export class ManualApplyForJob {
  static readonly type = ManualApplyActionTypes.ManualApplyForJob;

  constructor(public jobId: number, public coverLetterData?: CoverLetterApplyData) {
  }
}


export class ReapplyForJob {
  static readonly type = ManualApplyActionTypes.ReapplyForJob;

  constructor(public jobId: number, public coverLetterData?: CoverLetterApplyData) {
  }
}


export class ResetManualApplyState {
  static readonly type = ManualApplyActionTypes.ResetManualApplyState;

  constructor() {
  }
}


export class ChangeManualApplyValidationMessage {
  static readonly type = ManualApplyActionTypes.ChangeManualApplyValidationMessage;

  constructor(public message: string) {
  }
}


export class ChangeManualApplyPossibility {
  static readonly type = ManualApplyActionTypes.ChangeManualApplyPossibility;

  constructor(public jobData: any) {
  }
}


export type JobSeekerManualApplyActionUnion =
  | ReapplyForJob
  | ManualApplyForJob
  | ChangeManualApplyPossibility
  | ChangeManualApplyValidationMessage;
