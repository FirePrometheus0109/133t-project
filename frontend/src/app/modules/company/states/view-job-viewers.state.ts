import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { ViewJobViewerActions } from '../actions';
import { JobView } from '../models/job-view.model';
import { JobService } from '../services/job.service';


class ViewJobViewerStateModel extends BasePaginatedPageStateModel {
  results: Array<JobView>;
}


@State<ViewJobViewerStateModel>({
  name: 'ViewJobViewerPageState',
  defaults: DEFAULT_PAGINATED_STATE,
})
export class ViewJobViewerPageState extends BaseBlockablePageState {
  @Selector()
  static count(state: ViewJobViewerStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: ViewJobViewerStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: ViewJobViewerStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static results(state: ViewJobViewerStateModel): Array<any> {
    return state.results;
  }

  constructor(private jobService: JobService) {
    super();
  }

  @Action(ViewJobViewerActions.LoadJobViewers)
  loadJobsViewers(ctx: StateContext<ViewJobViewerStateModel>,
                  {id, limit, offset}: ViewJobViewerActions.LoadJobViewers) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getViewers(id, limit, offset).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          count: result.count,
          next: result.next,
          previous: result.previous,
          results: result.results,
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
          results: [],
        }));
      }),
    );
  }

  @Action(ViewJobViewerActions.ChangePagination)
  changePagination(ctx: StateContext<ViewJobViewerStateModel>,
                   {id, paginatedData}: ViewJobViewerActions.ChangePagination) {
    const limit = paginatedData.pageSize;
    const offset = paginatedData.pageIndex * paginatedData.pageSize;
    return ctx.dispatch(new ViewJobViewerActions.LoadJobViewers(id, limit, offset));
  }
}
