export enum CompanyDashboardActionTypes {
  LoadInitialData = '[Company Dashboard] LoadInitialData',
  ToggleSubscriptionPanel = '[Company Dashboard] ToggleSubscriptionPanel',
  LoadCandidatesActivity = '[Company Dashboard] LoadCandidatesActivity',
  SetCurrentPagination = '[Company Dashboard] SetCurrentPagination',
  LoadNewestJobs = '[Company Dashboard] LoadNewestJobs',
  LoadScoreCardData = '[Company Dashboard] LoadScoreCardData',
  SetScoreCardSettings = '[Company Dashboard] SetScoreCardSettings',
  ToggleScoreCardMode = '[Company Dashboard] ToggleScoreCardMode',
  LoadAllScoreCardData = '[Company Dashboard] LoadAllScoreCardData',
}


export class LoadInitialData {
  static readonly type = CompanyDashboardActionTypes.LoadInitialData;
}


export class SetScoreCardSettings {
  static readonly type = CompanyDashboardActionTypes.SetScoreCardSettings;

  constructor(public cardIds: Array<number>) {
  }
}


export class LoadScoreCardData {
  static readonly type = CompanyDashboardActionTypes.LoadScoreCardData;
}


export class LoadAllScoreCardData {
  static readonly type = CompanyDashboardActionTypes.LoadAllScoreCardData;
}


export class ToggleSubscriptionPanel {
  static readonly type = CompanyDashboardActionTypes.ToggleSubscriptionPanel;
}


export class ToggleScoreCardMode {
  static readonly type = CompanyDashboardActionTypes.ToggleScoreCardMode;
}


export class SetCurrentPagination {
  static readonly type = CompanyDashboardActionTypes.SetCurrentPagination;

  constructor(public params: object) {
  }
}


export class LoadCandidatesActivity {
  static readonly type = CompanyDashboardActionTypes.LoadCandidatesActivity;

  constructor(public params: object) {
  }
}


export class LoadNewestJobs {
  static readonly type = CompanyDashboardActionTypes.LoadNewestJobs;

  constructor(public params: object) {
  }
}


export type CompanyDashboardActionsUnion =
  | LoadAllScoreCardData
  | LoadNewestJobs
  | SetCurrentPagination
  | LoadCandidatesActivity
  | LoadInitialData
  | ToggleSubscriptionPanel
  | LoadScoreCardData
  | SetScoreCardSettings
  | ToggleScoreCardMode;
