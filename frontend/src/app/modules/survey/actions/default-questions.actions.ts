export enum DefaultQuestionsActionsTypes {
  LoadDefaultQuestionList = '[Default Question List] LoadDefaultQuestionList',
}

export class LoadDefaultQuestionList {
  static readonly type = DefaultQuestionsActionsTypes.LoadDefaultQuestionList;
}

export type DefaultQuestionsActionsUnion =
  | LoadDefaultQuestionList;
