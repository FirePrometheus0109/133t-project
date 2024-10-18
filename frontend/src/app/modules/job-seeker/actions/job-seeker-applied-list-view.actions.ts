export enum JobSeekerAppliedListTypes {
  LoadAnswersForJob = '[Job Seeker Applied List] LoadAnswersForJob',
}

export class LoadAnswersForJob {
  static readonly type = JobSeekerAppliedListTypes.LoadAnswersForJob;

  constructor(public jobId: number, public jsId: number) {
  }
}

export type JobSeekerAppliedListActionUnions =
  | LoadAnswersForJob;
