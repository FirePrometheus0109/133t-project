export enum ViewAnsweredQuestionnaireTypes {
  LoadAnswers = '[Candidate Page] Load Answers'
}

export class LoadAnswers {
  static readonly type = ViewAnsweredQuestionnaireTypes.LoadAnswers;

  constructor(public jobId: number, public jobSeekerId: number) {
  }
}

export type ViewAnsweredQuestionnaireUnion =
  | LoadAnswers;
