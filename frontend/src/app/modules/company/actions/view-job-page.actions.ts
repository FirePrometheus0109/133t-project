export enum ViewJobPageActionTypes {
  LoadInitialData = '[Job Page] LoadInitialData',
}

export class LoadInitialData {
  static readonly type = ViewJobPageActionTypes.LoadInitialData;

  constructor(public id: number) {
  }
}

export type ViewJobPageActionsUnion =
  | LoadInitialData;
