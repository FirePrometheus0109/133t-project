import {AnswerData} from '../models/answer.model';

export enum AnswersActionsTypes {
  SetAnswerToAnswersList = '[Answers] SetAnswerToAnswersList',
  SendAnswersList = '[Answers] SendAnswersList',
  ResetAnswerList = '[Answers] ResetAnswerList',
}

export class SetAnswerToAnswersList {
  static readonly type = AnswersActionsTypes.SetAnswerToAnswersList;

  constructor(public answerData: AnswerData) {
  }
}

export class SendAnswersList {
  static readonly type = AnswersActionsTypes.SendAnswersList;

  constructor(public jobId: number) {
  }
}

export class ResetAnswerList {
  static readonly type = AnswersActionsTypes.ResetAnswerList;
}

export type AnswersActionsUnion =
  | ResetAnswerList
  | SendAnswersList
  | SetAnswerToAnswersList;
