export enum QuickViewCandidateActionTypes {
  LoadCandidateData = '[Quick View Candidate] LoadCompaniesData',
  ChangeCandidate = '[Quick View Candidate] ChangeCandidate',
}

export class LoadCandidateData {
  static readonly type = QuickViewCandidateActionTypes.LoadCandidateData;

  constructor(public params?: object) {
  }
}

export class ChangeCandidate {
  static readonly type = QuickViewCandidateActionTypes.ChangeCandidate;

  constructor(public params?: object) {
  }
}

export type QuickViewCandidateActionUnion =
  | ChangeCandidate
  | LoadCandidateData;
