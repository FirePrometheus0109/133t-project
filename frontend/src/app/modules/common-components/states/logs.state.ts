import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { LogsActions } from '../actions/index';
import { LogItem } from '../models/log.model';
import { LogsService } from '../services/logs.service';


class LogsStateModel extends BasePaginatedPageStateModel {
  logs: Array<LogItem>;
  logType: string;
  sourceId: number;
}


export const DEFAULT_LOGS_STATE = Object.assign({
  logs: [],
  logType: '',
  sourceId: null,
}, DEFAULT_PAGINATED_STATE);


@State<LogsStateModel>({
  name: 'LogsState',
  defaults: DEFAULT_LOGS_STATE,
})

export class LogsState extends BaseBlockablePageState {
  @Selector()
  static count(state: LogsStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: LogsStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: LogsStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static results(state: LogsStateModel): Array<any> {
    return state.results;
  }

  @Selector()
  static logs(state: LogsStateModel): LogItem[] {
    return state.logs;
  }

  @Selector()
  static logsCount(state: LogsStateModel): number {
    return state.logs.length;
  }

  @Selector()
  static sourceId(state: LogsStateModel): number {
    return state.sourceId;
  }

  constructor(private logsService: LogsService) {
    super();
  }

  @Action(LogsActions.LoadLogsData)
  loadLogsData(ctx: StateContext<LogsStateModel>, {sourceId, params}: LogsActions.LoadLogsData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    Object.assign(params, {ct_model: state.logType, object_id: sourceId});
    return this.logsService.getLogsData(params).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          sourceId: sourceId,
          count: result.count,
          next: result.next,
          previous: result.previous,
          logs: result.results,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          count: 0,
          next: null,
          previous: null,
          logs: [],
        }));
      }),
    );
  }

  @Action(LogsActions.DeleteLog)
  deleteLog(ctx: StateContext<LogsStateModel>,
            {logId}: LogsActions.DeleteLog) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.logsService.deleteLog(logId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done'
        });
        return ctx.dispatch(new LogsActions.LoadLogsData(state.sourceId, {limit: state.limit, offset: state.offset}));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(LogsActions.SetLogType)
  setLogType(ctx: StateContext<LogsStateModel>,
             {logType}: LogsActions.SetLogType) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      logType: logType
    });
  }

  @Action(LogsActions.ResetLogState)
  resetLogState(ctx: StateContext<LogsStateModel>) {
    return ctx.setState({
      ...DEFAULT_LOGS_STATE,
    });
  }

  @Action(LogsActions.SetCurrentPagination)
  setCurrentPagination(ctx: StateContext<LogsStateModel>,
                       {params}: LogsActions.SetCurrentPagination) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      ...params,
    });
    state = ctx.getState();
    return ctx.dispatch(new LogsActions.LoadLogsData(state.sourceId, {limit: state.limit, offset: state.offset}));
  }
}
