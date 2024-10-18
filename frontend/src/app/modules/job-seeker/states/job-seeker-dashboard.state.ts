import { Action, Selector, State, StateContext } from '@ngxs/store';
import { forkJoin, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';
import { CoreActions } from '../../core/actions';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { JobSeekerDashboardActions } from '../actions';
import { JobSeekerAutoApplyProgressItem } from '../models/job-seeker-auto-apply-progress.model';
import { JobSeekerLastViewsItemModel } from '../models/job-seeker-last-views.model';
import { JobSeekerService } from '../services/job-seeker.service';


class JobSeekerDashboardStateModel extends BasePaginatedPageStateModel {
  status: string;
  errors: object;
  lastViews: JobSeekerLastViewsItemModel[];
  autoApplyProgressList: JobSeekerAutoApplyProgressItem[];
}


export const DEFAULT_JOB_SEEKER_DASHBOARD_STATE = Object.assign({
  status: '',
  errors: null,
  lastViews: [],
  autoApplyProgressList: []
}, DEFAULT_PAGINATED_STATE);


@State<JobSeekerDashboardStateModel>({
  name: 'JobSeekerDashboardPage',
  defaults: DEFAULT_JOB_SEEKER_DASHBOARD_STATE,
})
export class JobSeekerDashboardState {

  @Selector()
  static lastViews(state: any) {
    return state.lastViews;
  }

  @Selector()
  static count(state: any) {
    return state.count;
  }

  @Selector()
  static pageSizeOptions(state: any) {
    return state.pageSizeOptions;
  }

  @Selector()
  static pageSize(state: any) {
    return state.pageSize;
  }

  @Selector()
  static autoApplyProgressList(state: any) {
    return state.autoApplyProgressList;
  }

  constructor(private jobSeekerService: JobSeekerService) {
  }

  @Action(JobSeekerDashboardActions.LoadInitialData)
  loadInitialData(ctx: StateContext<JobSeekerDashboardStateModel>,
                  {jsId}: JobSeekerDashboardActions.LoadInitialData) {
    return forkJoin(
      ctx.dispatch(new CoreActions.ListFavoriteJobs(jsId, {limit: environment.savedJobsLimitOnDashboard})),
      ctx.dispatch(new JobSeekerDashboardActions.GetLastViewsList(jsId)),
      ctx.dispatch(new JobSeekerDashboardActions.GetAutoApplyProgress()),
    );
  }

  @Action(JobSeekerDashboardActions.GetLastViewsList)
  getLastViewsList(ctx, {jsId, params}: JobSeekerDashboardActions.GetLastViewsList) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobSeekerService.getLastViewsForJS(jsId, params).pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          count: result.count,
          next: result.next,
          previous: result.previous,
          lastViews: result.results,
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
          lastViews: [],
        }));
      }),
    );
  }

  @Action(JobSeekerDashboardActions.SetCurrentPagination)
  setCurrentPagination(ctx, {params}: JobSeekerDashboardActions.SetCurrentPagination) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      ...params
    });
  }

  @Action(JobSeekerDashboardActions.GetAutoApplyProgress)
  getAutoApplyProgress(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobSeekerService.getAutoApplyStats().pipe(
      tap((result: JobSeekerAutoApplyProgressItem[]) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          autoApplyProgressList: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          autoApplyProgressList: [],
        }));
      }),
    );
  }
}
