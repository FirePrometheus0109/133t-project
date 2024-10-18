import {PageEvent} from '@angular/material';

export enum ViewJobViewerActionTypes {
  LoadJobViewers = '[Job Viewer Page] LoadJobViewers',
  ChangePagination = '[Job Viewer Page] ChangePagination',
}

export class LoadJobViewers {
  static readonly type = ViewJobViewerActionTypes.LoadJobViewers;

  constructor(public id: number, public limit: number = 10,
              public offset: number = 0) {
  }
}

export class ChangePagination {
  static readonly type = ViewJobViewerActionTypes.ChangePagination;

  constructor(public id: number, public paginatedData: PageEvent) {
  }
}

export type ViewJobViewerActionsUnion =
  | LoadJobViewers
  | ChangePagination;
