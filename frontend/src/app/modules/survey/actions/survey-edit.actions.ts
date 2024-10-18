import { EditMode } from '../models/edit-mode.model';
import { Question } from '../models/question.model';
import { Survey } from '../models/survey.model';


export enum SurveyEditActionsTypes {
  SetCreateQuestionMode = '[Survey Edit] SetCreateQuestionMode',
  SetViewQuestionMode = '[Survey Edit] SetViewQuestionMode',
  SetEditQuestionMode = '[Survey Edit] SetEditQuestionMode',
  CreateNewSurvey = '[Survey Edit] CreateNewSurvey',
  DeleteSurvey = '[Survey Edit] DeleteSurvey',
  SetSurveyToEdit = '[Survey Edit] SetSurveyToEdit',
  UpdateSurveyTitle = '[Survey Edit] UpdateSurveyTitle',
  SetQuestionEditMode = '[Survey Edit] SetQuestionEditMode',
  UpdateQuestionInSurvey = '[Survey Edit] UpdateQuestionInSurvey',
  DeleteQuestionFromSurvey = '[Survey Edit] DeleteQuestionFromSurvey',
  SaveNewlyCreatedQuestions = '[Survey Edit] SaveNewlyCreatedQuestions',
  SaveQuestionsFromSelected = '[Survey Edit] SaveQuestionsFromSelected',
}


export class SetCreateQuestionMode {
  static readonly type = SurveyEditActionsTypes.SetCreateQuestionMode;

  constructor(public value: boolean) {
  }
}


export class SetViewQuestionMode {
  static readonly type = SurveyEditActionsTypes.SetViewQuestionMode;

  constructor(public value: boolean) {
  }
}


export class SetEditQuestionMode {
  static readonly type = SurveyEditActionsTypes.SetEditQuestionMode;

  constructor(public value: EditMode) {
  }
}


export class CreateNewSurvey {
  static readonly type = SurveyEditActionsTypes.CreateNewSurvey;

  constructor(public newSurvey: Survey) {
  }
}


export class UpdateSurveyTitle {
  static readonly type = SurveyEditActionsTypes.UpdateSurveyTitle;

  constructor(public survey: Survey) {
  }
}


export class DeleteSurvey {
  static readonly type = SurveyEditActionsTypes.DeleteSurvey;

  constructor(public surveyId: number) {
  }
}


export class SetSurveyToEdit {
  static readonly type = SurveyEditActionsTypes.SetSurveyToEdit;

  constructor(public survey: Survey) {
  }
}


export class SetQuestionEditMode {
  static readonly type = SurveyEditActionsTypes.SetQuestionEditMode;

  constructor(public value: EditMode) {
  }
}


export class UpdateQuestionInSurvey {
  static readonly type = SurveyEditActionsTypes.UpdateQuestionInSurvey;

  constructor(public surveyId: number, public questionData: Question) {
  }
}


export class DeleteQuestionFromSurvey {
  static readonly type = SurveyEditActionsTypes.DeleteQuestionFromSurvey;

  constructor(public surveyId: number, public questionId: number) {
  }
}


export class SaveNewlyCreatedQuestions {
  static readonly type = SurveyEditActionsTypes.SaveNewlyCreatedQuestions;

  constructor(public surveyId: number, public questionList: Array<Question>) {
  }
}


export class SaveQuestionsFromSelected {
  static readonly type = SurveyEditActionsTypes.SaveQuestionsFromSelected;

  constructor(public surveyId: number, public questionList: Array<number>) {
  }
}


export type SurveyEditActionsUnion =
  | SaveQuestionsFromSelected
  | SaveNewlyCreatedQuestions
  | DeleteQuestionFromSurvey
  | UpdateQuestionInSurvey
  | SetQuestionEditMode
  | UpdateSurveyTitle
  | SetSurveyToEdit
  | DeleteSurvey
  | CreateNewSurvey
  | SetEditQuestionMode
  | SetViewQuestionMode
  | SetCreateQuestionMode;
