import {PageEvent} from '@angular/material';

export enum ViewCompanyListPageActionTypes {
  LoadCompaniesData = '[View Company List Page] LoadCompaniesData',
  ChangePagination = '[View Company List Page] ChangePagination',
}

export class LoadCompaniesData {
  static readonly type = ViewCompanyListPageActionTypes.LoadCompaniesData;

  constructor(public limit: number, public offset: number) {
  }
}

export class ChangePagination {
  static readonly type = ViewCompanyListPageActionTypes.ChangePagination;

  constructor(public paginatedData: PageEvent) {
  }
}

export type ViewCompanyListPageActionUnion =
  | LoadCompaniesData
  | ChangePagination;
