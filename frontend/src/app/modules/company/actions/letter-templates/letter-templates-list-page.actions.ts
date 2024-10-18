export enum LetterTemplatesListActionTypes {
  GetLetterTemplatesList = '[Letter Templates List] GetLetterTemplatesList',
  UpdateListParams = '[Letter Templates List] UpdateListParams',
  DeleteLetterTemplate = '[Letter Templates List] DeleteLetterTemplate',
}


export class GetLetterTemplatesList {
  static readonly type = LetterTemplatesListActionTypes.GetLetterTemplatesList;

  constructor(private params?: object) {
  }
}


export class UpdateListParams {
  static readonly type = LetterTemplatesListActionTypes.UpdateListParams;

  constructor(private params?: object) {
  }
}


export class DeleteLetterTemplate {
  static readonly type = LetterTemplatesListActionTypes.DeleteLetterTemplate;

  constructor(private letterTemplateId: number) {
  }
}


export type LetterTemplatesListActionUnion =
  | DeleteLetterTemplate
  | GetLetterTemplatesList
  | UpdateListParams;
