import { PageEvent } from '@angular/material';
import { EditMode } from '../models/edit-mode.model';
import { Question } from '../models/question.model';


export enum SavedQuestionsActionsTypes {
  LoadSavedQuestionList = '[Saved Question List] LoadSavedQuestionList',
  CreateNewQuestion = '[Saved Question List] CreateNewQuestion',
  SetCreationMode = '[Saved Question List] SetCreationMode',
  SetEditMode = '[Saved Question List] SetEditMode',
  UpdateSavedQuestion = '[Saved Question List] UpdateSavedQuestion',
  DeleteSavedQuestion = '[Saved Question List] DeleteSavedQuestion',
  ChangePagination = '[Saved Question List] ChangePagination',
}


export class LoadSavedQuestionList {
  static readonly type = SavedQuestionsActionsTypes.LoadSavedQuestionList;

  constructor(public limit: number, public offset: number) {
  }
}


export class CreateNewQuestion {
  static readonly type = SavedQuestionsActionsTypes.CreateNewQuestion;

  constructor(public questionData: Question) {
  }
}


export class UpdateSavedQuestion {
  static readonly type = SavedQuestionsActionsTypes.UpdateSavedQuestion;

  constructor(public questionData: Question) {
  }
}


export class SetCreationMode {
  static readonly type = SavedQuestionsActionsTypes.SetCreationMode;

  constructor(public value: boolean) {
  }
}


export class SetEditMode {
  static readonly type = SavedQuestionsActionsTypes.SetEditMode;

  constructor(public value: EditMode) {
  }
}


export class DeleteSavedQuestion {
  static readonly type = SavedQuestionsActionsTypes.DeleteSavedQuestion;

  constructor(public questionId: number) {
  }
}


export class ChangePagination {
  static readonly type = SavedQuestionsActionsTypes.ChangePagination;

  constructor(public paginatedData: PageEvent) {
  }
}


export type SavedQuestionsActionsUnion =
  | ChangePagination
  | DeleteSavedQuestion
  | UpdateSavedQuestion
  | SetEditMode
  | SetCreationMode
  | CreateNewQuestion
  | LoadSavedQuestionList;
