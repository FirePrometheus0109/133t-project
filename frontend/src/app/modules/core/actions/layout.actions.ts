export enum LayoutActionTypes {
  OpenSidenav = '[Layout] OpenSidenav',
  CloseSidenav = '[Layout] CloseSidenav',
}

export class OpenSidenav {
  static readonly type = LayoutActionTypes.OpenSidenav;
}

export class CloseSidenav {
  static readonly type = LayoutActionTypes.CloseSidenav;
}

export type LayoutActionsUnion =
  | OpenSidenav
  | CloseSidenav;
