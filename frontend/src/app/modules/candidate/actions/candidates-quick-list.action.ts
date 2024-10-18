export enum CandidatesQuickListActionTypes {
  GetCandidatesQuickList = '[Candidates Quick List] GetCandidatesQuickList',
  UpdateQuickListParams = '[Candidates Quick List] UpdateQuickListParams',
}


export class GetCandidatesQuickList {
  static readonly type = CandidatesQuickListActionTypes.GetCandidatesQuickList;

  constructor(public params?: object) {
  }
}


export class UpdateQuickListParams {
  static readonly type = CandidatesQuickListActionTypes.UpdateQuickListParams;

  constructor(public params?: object) {
  }
}


export type CandidatesQuickListActionUnion =
  | GetCandidatesQuickList
  | UpdateQuickListParams;
