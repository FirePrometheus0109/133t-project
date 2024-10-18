import { LetterTemplateItem } from '../../models/letter-templates.model';


export enum LetterTemplateManageActionsTypes {
  LoadLetterTemplatesEventTypes = '[Manage Letter Template] LoadLetterTemplatesEventTypes',
  SetCreateMode = '[Manage Letter Template] SetCreateMode',
  SetEditMode = '[Manage Letter Template] SetEditMode',
  SetViewMode = '[Manage Letter Template] SetViewMode',
  CreateLetterTemplate = '[Manage Letter Template] CreateLetterTemplate',
  LoadLetterTemplateData = '[Manage Letter Template] LoadLetterTemplateData',
  ResetCurrentLetterTemplate = '[Manage Letter Template] ResetCurrentLetterTemplate',
  SaveLetterTemplate = '[Manage Letter Template] SaveLetterTemplate',
}


export class LoadLetterTemplatesEventTypes {
  static readonly type = LetterTemplateManageActionsTypes.LoadLetterTemplatesEventTypes;
}


export class SetCreateMode {
  static readonly type = LetterTemplateManageActionsTypes.SetCreateMode;

  constructor(private value: boolean) {
  }
}


export class SetEditMode {
  static readonly type = LetterTemplateManageActionsTypes.SetEditMode;

  constructor(private value: boolean) {
  }
}


export class SetViewMode {
  static readonly type = LetterTemplateManageActionsTypes.SetViewMode;

  constructor(private value: boolean) {
  }
}


export class CreateLetterTemplate {
  static readonly type = LetterTemplateManageActionsTypes.CreateLetterTemplate;

  constructor(private letterTemplate: LetterTemplateItem) {
  }
}


export class LoadLetterTemplateData {
  static readonly type = LetterTemplateManageActionsTypes.LoadLetterTemplateData;

  constructor(private letterTemplateId: number) {
  }
}


export class ResetCurrentLetterTemplate {
  static readonly type = LetterTemplateManageActionsTypes.ResetCurrentLetterTemplate;
}


export class SaveLetterTemplate {
  static readonly type = LetterTemplateManageActionsTypes.SaveLetterTemplate;

  constructor(private letterTemplateId: number, private letterTemplate: LetterTemplateItem) {
  }
}


export type LetterTemplateManageActionsUnion =
  | SaveLetterTemplate
  | ResetCurrentLetterTemplate
  | LoadLetterTemplateData
  | CreateLetterTemplate
  | LoadLetterTemplatesEventTypes
  | SetCreateMode
  | SetEditMode
  | SetViewMode;
