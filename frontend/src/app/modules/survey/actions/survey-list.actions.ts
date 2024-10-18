import { PageEvent } from '@angular/material';
import { Question } from '../models/question.model';
import { Survey } from '../models/survey.model';


export enum SurveyListActionsTypes {
  LoadSurveyList = '[Survey List] LoadSurveyList',
  ChangePagination = '[Survey List] ChangePagination',
  SetCreationMode = '[Survey List] SetCreationMode',
  SetCurrentSurvey = '[Survey List] SetCurrentSurvey',
  SetViewMode = '[Survey List] SetViewMode',
  SetEditMode = '[Survey List] SetEditMode',
  SetModalMode = '[Survey List] SetModalMode',
  DeleteSurvey = '[Survey List] DeleteSurvey',
  SearchSurvey = '[Survey List] SearchSurvey',
  SetCreateQuestionMode = '[Survey List] SetCreateQuestionMode',
  CreateNewSurvey = '[Survey List] CreateNewSurvey',
  UpdateSurveyList = '[Survey List] UpdateSurveyList',
  UpdateCurrentSurvey = '[Survey List] UpdateCurrentSurvey',
  GetSurvey = '[Survey List] GetSurvey',
  SetJobEditMode = '[Survey List] SetJobEditMode',
  UpdateSurveyForJobEdit = '[Survey List] UpdateSurveyForJobEdit',
  UpdateQuestionInSurveyForJobEdit = '[Survey List] UpdateQuestionInSurveyForJobEdit',
  DeleteQuestionFromSurveyForJobEdit = '[Survey List] DeleteQuestionFromSurveyForJobEdit',
}


export class LoadSurveyList {
  static readonly type = SurveyListActionsTypes.LoadSurveyList;

  constructor(public limit: number, public offset: number, public search?: string) {
  }
}


export class ChangePagination {
  static readonly type = SurveyListActionsTypes.ChangePagination;

  constructor(public paginatedData: PageEvent) {
  }
}


export class SetCreationMode {
  static readonly type = SurveyListActionsTypes.SetCreationMode;

  constructor(public value: boolean) {
  }
}


export class SetCreateQuestionMode {
  static readonly type = SurveyListActionsTypes.SetCreateQuestionMode;

  constructor(public value: boolean) {
  }
}


export class SetViewMode {
  static readonly type = SurveyListActionsTypes.SetViewMode;

  constructor(public value: boolean) {
  }
}


export class SetEditMode {
  static readonly type = SurveyListActionsTypes.SetEditMode;

  constructor(public value: boolean) {
  }
}


export class SetModalMode {
  static readonly type = SurveyListActionsTypes.SetModalMode;

  constructor(public value: boolean) {
  }
}


export class SetJobEditMode {
  static readonly type = SurveyListActionsTypes.SetJobEditMode;

  constructor(public value: boolean) {
  }
}


export class SetCurrentSurvey {
  static readonly type = SurveyListActionsTypes.SetCurrentSurvey;

  constructor(public survey: Survey) {
  }
}


export class CreateNewSurvey {
  static readonly type = SurveyListActionsTypes.CreateNewSurvey;

  constructor(public survey: Survey) {
  }
}


export class DeleteSurvey {
  static readonly type = SurveyListActionsTypes.DeleteSurvey;

  constructor(public surveyId: number) {
  }
}


export class GetSurvey {
  static readonly type = SurveyListActionsTypes.GetSurvey;

  constructor(public surveyId: number) {
  }
}


export class UpdateCurrentSurvey {
  static readonly type = SurveyListActionsTypes.UpdateCurrentSurvey;

  constructor(public surveyId: number) {
  }
}


export class UpdateSurveyForJobEdit {
  static readonly type = SurveyListActionsTypes.UpdateSurveyForJobEdit;

  constructor(public questions: Array<Question>) {
  }
}


export class UpdateQuestionInSurveyForJobEdit {
  static readonly type = SurveyListActionsTypes.UpdateQuestionInSurveyForJobEdit;

  constructor(public updatedQuestionData: Question) {
  }
}


export class DeleteQuestionFromSurveyForJobEdit {
  static readonly type = SurveyListActionsTypes.DeleteQuestionFromSurveyForJobEdit;

  constructor(public questionId: number) {
  }
}


export class SearchSurvey {
  static readonly type = SurveyListActionsTypes.SearchSurvey;

  constructor(public searchTitle: string) {
  }
}


export class UpdateSurveyList {
  static readonly type = SurveyListActionsTypes.UpdateSurveyList;
}


export type SurveyListActionsUnion =
  | GetSurvey
  | UpdateCurrentSurvey
  | UpdateSurveyList
  | CreateNewSurvey
  | SetCreateQuestionMode
  | SearchSurvey
  | DeleteSurvey
  | SetModalMode
  | SetJobEditMode
  | DeleteQuestionFromSurveyForJobEdit
  | UpdateQuestionInSurveyForJobEdit
  | UpdateSurveyForJobEdit
  | SetEditMode
  | SetViewMode
  | SetCurrentSurvey
  | SetCreationMode
  | ChangePagination
  | LoadSurveyList;
