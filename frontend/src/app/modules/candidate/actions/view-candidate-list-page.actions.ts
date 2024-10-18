import { Filter } from '../../shared/models/filters.model';
import { CandidateStatus } from '../models/candidate-item.model';
import { CandidateListMode } from '../models/candidate-parametr.model';


export enum ViewCandidateListPageActionTypes {
  InitCandidateList = '[View Candidate List Page] InitCandidateList',
  LoadCandidateData = '[View Candidate List Page] LoadCompaniesData',
  ToggleFilterList = '[View Candidate List Page] ToggleFilterList',
  ChangeSelectedFilters = '[View Candidate List Page] ChangeSelectedFilters',
  ClearFilters = '[View Candidate List Page] ClearFilters',
  SetCurrentSortingField = '[View Candidate List Page] SetCurrentSortingField',
  SetCurrentPagination = '[View Candidate List Page] SetCurrentPagination',
  InitJobCandidateList = '[View Candidate List Page] InitJobCandidateList',
  DownloadCandidatesToCSV = '[View Candidate List Page] DownloadCandidatesToCSV',
  UpdateParams = '[View Candidate List Page] UpdateParams',
  RemoveSelectedFilter = '[View Candidate List Page] RemoveSelectedFilter',
}


export class InitCandidateList {
  static readonly type = ViewCandidateListPageActionTypes.InitCandidateList;

  constructor(public mode: CandidateListMode, public userId?: number) {
  }
}


export class InitJobCandidateList {
  static readonly type = ViewCandidateListPageActionTypes.InitJobCandidateList;

  constructor(public status: CandidateStatus) {
  }
}


export class LoadCandidateData {
  static readonly type = ViewCandidateListPageActionTypes.LoadCandidateData;

  constructor(public params?: object, public limit?: number, public offset?: number) {
  }
}


export class SetCurrentSortingField {
  static readonly type = ViewCandidateListPageActionTypes.SetCurrentSortingField;

  constructor(public params: object) {
  }
}


export class SetCurrentPagination {
  static readonly type = ViewCandidateListPageActionTypes.SetCurrentPagination;

  constructor(public params: object) {
  }
}


export class ToggleFilterList {
  static readonly type = ViewCandidateListPageActionTypes.ToggleFilterList;
}


export class ChangeSelectedFilters {
  static readonly type = ViewCandidateListPageActionTypes.ChangeSelectedFilters;

  constructor(public filter: Filter) {
  }
}


export class RemoveSelectedFilter {
  static readonly type = ViewCandidateListPageActionTypes.RemoveSelectedFilter;

  constructor(public filter: Filter) {
  }
}


export class ClearFilters {
  static readonly type = ViewCandidateListPageActionTypes.ClearFilters;
}


export class DownloadCandidatesToCSV {
  static readonly type = ViewCandidateListPageActionTypes.DownloadCandidatesToCSV;

  constructor(public selectedCandidates: number[]) {
  }
}


export class UpdateParams {
  static readonly type = ViewCandidateListPageActionTypes.UpdateParams;

  constructor(public params: object, public changeType: string) {
  }
}


export type ViewCompanyListPageActionUnion =
  | RemoveSelectedFilter
  | UpdateParams
  | DownloadCandidatesToCSV
  | InitCandidateList
  | SetCurrentPagination
  | SetCurrentSortingField
  | LoadCandidateData
  | ToggleFilterList
  | ChangeSelectedFilters
  | ClearFilters
  | InitJobCandidateList;
