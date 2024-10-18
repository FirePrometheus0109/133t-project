export enum LogsActionTypes {
  LoadLogsData = '[Logs] LoadLogsData',
  DeleteLog = '[Logs] DeleteLog',
  SetLogType = '[Logs] SetLogType',
  ResetLogState = '[Logs] ResetLogState',
  SetCurrentPagination = '[Logs] SetCurrentPagination',
}


export class LoadLogsData {
  static readonly type = LogsActionTypes.LoadLogsData;

  constructor(public sourceId: number, public params?: any) {
  }
}


export class DeleteLog {
  static readonly type = LogsActionTypes.DeleteLog;

  constructor(public logId: number) {
  }
}


export class SetLogType {
  static readonly type = LogsActionTypes.SetLogType;

  constructor(public logType: string) {
  }
}


export class ResetLogState {
  static readonly type = LogsActionTypes.ResetLogState;
}


export class SetCurrentPagination {
  static readonly type = LogsActionTypes.SetCurrentPagination;

  constructor(public params: object) {
  }
}


export type LogsActionUnion =
  | SetCurrentPagination
  | ResetLogState
  | SetLogType
  | DeleteLog
  | LoadLogsData;
