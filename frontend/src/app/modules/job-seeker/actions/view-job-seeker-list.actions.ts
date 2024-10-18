import { Filter } from '../../shared/models/filters.model';
import { JobSeekerListMode } from '../models/job-seeker-list-fitlers.model';


export enum ViewJobSeekerListPageActionTypes {
  InitJobSeekerList = '[View Job Seeker List Page] InitJobSeekerList',
  LoadJobSeekerData = '[View Job Seeker List Page] LoadJobSeekerData',
  ToggleFilterList = '[View Job Seeker List Page] ToggleFilterList',
  ChangeSelectedFilters = '[View Job Seeker List Page] ChangeSelectedFilters',
  RemoveSelectedFilter = '[View Job Seeker List Page] RemoveSelectedFilter',
  ClearFilters = '[View Job Seeker List Page] ClearFilters',
  SetCurrentSortingField = '[View Job Seeker List Page] SetCurrentSortingField',
  SetCurrentPagination = '[View Job Seeker List Page] SetCurrentPagination',
  UpdateParams = '[View Job Seeker List Page] UpdateParams',
  SetGlobalFilterOnInit = '[View Job Seeker List Page] SetGlobalFilterOnInit',
}


export class InitJobSeekerList {
  static readonly type = ViewJobSeekerListPageActionTypes.InitJobSeekerList;

  constructor(public mode?: JobSeekerListMode, public params?: object) {
  }
}


export class LoadJobSeekerData {
  static readonly type = ViewJobSeekerListPageActionTypes.LoadJobSeekerData;

  constructor(public params?: object, public limit?: number, public offset?: number) {
  }
}


export class SetCurrentSortingField {
  static readonly type = ViewJobSeekerListPageActionTypes.SetCurrentSortingField;

  constructor(public params: object) {
  }
}


export class SetCurrentPagination {
  static readonly type = ViewJobSeekerListPageActionTypes.SetCurrentPagination;

  constructor(public params: object) {
  }
}


export class ToggleFilterList {
  static readonly type = ViewJobSeekerListPageActionTypes.ToggleFilterList;
}


export class ChangeSelectedFilters {
  static readonly type = ViewJobSeekerListPageActionTypes.ChangeSelectedFilters;

  constructor(public filter: Filter) {
  }
}


export class RemoveSelectedFilter {
  static readonly type = ViewJobSeekerListPageActionTypes.RemoveSelectedFilter;

  constructor(public filter: Filter) {
  }
}


export class ClearFilters {
  static readonly type = ViewJobSeekerListPageActionTypes.ClearFilters;
}


export class UpdateParams {
  static readonly type = ViewJobSeekerListPageActionTypes.UpdateParams;

  constructor(public params?: any, public changeType?: string) {
  }
}


export class SetGlobalFilterOnInit {
  static readonly type = ViewJobSeekerListPageActionTypes.SetGlobalFilterOnInit;

  constructor(public filter: Filter) {
  }
}


export type ViewCompanyListPageActionUnion =
  | SetGlobalFilterOnInit
  | UpdateParams
  | InitJobSeekerList
  | SetCurrentPagination
  | SetCurrentSortingField
  | LoadJobSeekerData
  | ToggleFilterList
  | ChangeSelectedFilters
  | RemoveSelectedFilter
  | ClearFilters;
