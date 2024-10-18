import { DateBasis } from '../../shared/enums/company-reports.enums';

export enum CompanyReportsActionTypes {
  InitCompanyId = '[Company Reports] InitCompanyId',
  InitReportData = '[Company Reports] InitReportData',
  LoadGraphData = '[Company Reports] LoadGraphData',
  ChangeGraphDateBasic = '[Company Reports] ChangeGraphDateBasic',
  MoveGraphToPast = '[Company Reports] MoveGraphToPast',
  MoveGraphToFuture = '[Company Reports] MoveGraphToFuture',
  LoadRecruiterActivity = '[Company Reports] LoadRecruiterActivity',
  LoadWorkflowStats = '[Company Reports] LoadWorkflowStats',
  ChangeWorkflowFilter =  '[Company Reports] ChangeWorkflowFilter',
}

export class InitReportData {
  static readonly type = CompanyReportsActionTypes.InitReportData;

  constructor() {
  }
}

export class InitCompanyId {
  static readonly type = CompanyReportsActionTypes.InitCompanyId;

  constructor(public companyId: number) {
  }
}

export class LoadWorkflowStats {
  static readonly type = CompanyReportsActionTypes.LoadWorkflowStats;

  constructor() {
  }
}


export class LoadRecruiterActivity {
  static readonly type = CompanyReportsActionTypes.LoadRecruiterActivity;

  constructor() {
  }
}


export class LoadGraphData {
  static readonly type = CompanyReportsActionTypes.LoadGraphData;
}

export class ChangeGraphDateBasic {
  static readonly type = CompanyReportsActionTypes.ChangeGraphDateBasic;

  constructor(public basic: DateBasis) {
  }
}

export class ChangeWorkflowFilter {
  static readonly type = CompanyReportsActionTypes.ChangeWorkflowFilter;

  constructor(public filter: ChangeWorkflowFilter) {
  }
}

export class MoveGraphToPast {
  static readonly type = CompanyReportsActionTypes.MoveGraphToPast;
  constructor() {
  }
}

export class MoveGraphToFuture {
  static readonly type = CompanyReportsActionTypes.MoveGraphToFuture;
  constructor() {
  }
}


export type CompanyReportsActionUnion =
  | InitReportData
  | LoadGraphData
  | ChangeGraphDateBasic
  | InitCompanyId
  | MoveGraphToPast
  | MoveGraphToFuture
  | LoadRecruiterActivity
  | LoadWorkflowStats
  | ChangeWorkflowFilter;
