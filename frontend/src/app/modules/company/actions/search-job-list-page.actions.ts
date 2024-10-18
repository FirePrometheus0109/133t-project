import { Filter } from '../../shared/models/filters.model';


export enum SearchJobListPageActionTypes {
  LoadJobsData = '[Search Job Page] LoadJobData',
  ToggleFilterList = '[Search Job Page] ToggleFilterList',
  ClearFilters = '[Search Job Page] ClearFilters',
  ChangeSelectedFilters = '[Search Job Page] ChangeSelectedFilters',
  RemoveSelectedFilter = '[Search Job Page] RemoveSelectedFilter',
  UpdateParams = '[Search Job Page] UpdateParams',
  LoadCompanies = '[Search Job Page] LoadCompanies',
  LoadCompaniesExclude = '[Search Job Page] LoadCompaniesExclude',
  LoadCompaniesInclude = '[Search Job Page] LoadCompaniesInclude',
  SetSelectedFiltersOnInit = '[Search Job Page] SetSelectedFiltersOnInit',
}


export class LoadJobsData {
  static readonly type = SearchJobListPageActionTypes.LoadJobsData;

  constructor(public params?: object) {
  }
}


export class ToggleFilterList {
  static readonly type = SearchJobListPageActionTypes.ToggleFilterList;
}


export class ClearFilters {
  static readonly type = SearchJobListPageActionTypes.ClearFilters;
}


export class ChangeSelectedFilters {
  static readonly type = SearchJobListPageActionTypes.ChangeSelectedFilters;

  constructor(public filter: Filter) {
  }
}


export class SetSelectedFiltersOnInit {
  static readonly type = SearchJobListPageActionTypes.SetSelectedFiltersOnInit;

  constructor(public filter: Filter) {
  }
}


export class RemoveSelectedFilter {
  static readonly type = SearchJobListPageActionTypes.RemoveSelectedFilter;

  constructor(public filter: Filter) {
  }
}


export class UpdateParams {
  static readonly type = SearchJobListPageActionTypes.UpdateParams;

  constructor(public params?: any, public changeType?: string) {
  }
}


export class LoadCompanies {
  static readonly type = SearchJobListPageActionTypes.LoadCompanies;

  constructor(public search?: string, public companySelectionType?: string) {
  }
}


export class LoadCompaniesExclude {
  static readonly type = SearchJobListPageActionTypes.LoadCompaniesExclude;

  constructor(public search?: string) {
  }
}


export class LoadCompaniesInclude {
  static readonly type = SearchJobListPageActionTypes.LoadCompaniesInclude;

  constructor(public search?: string) {
  }
}


export type SearchJobListPageActionUnion =
  | SetSelectedFiltersOnInit
  | LoadCompaniesInclude
  | LoadCompaniesExclude
  | LoadCompanies
  | UpdateParams
  | RemoveSelectedFilter
  | ChangeSelectedFilters
  | ClearFilters
  | ToggleFilterList
  | LoadJobsData;
