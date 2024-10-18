import { Action, Selector, State, StateContext } from '@ngxs/store';
import { saveAs } from 'file-saver';
import * as moment from 'moment';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import * as CoreActions from '../../core/actions/core.actions';
import { GridViewHelper } from '../../shared/helpers/grid-view.helper';
import { JobSortingTypes, SortingFilter } from '../../shared/models/filters.model';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { ViewJobListPageActions } from '../actions';
import { JobItem } from '../models/job.model';
import { CompanyService } from '../services/company.service';
import { JobService } from '../services/job.service';


class ViewJobListPageStateModel extends BasePaginatedPageStateModel {
  results: object[];
  jobSortingFilter: SortingFilter[];
  params: object;
  jobAuthors: object[];
}


export const DEFAULT_COMPANY_PROFILE_PAGE_STATE = Object.assign({
  jobSortingFilter: [
    {value: JobSortingTypes.DATE, viewValue: 'by date'},
    {value: JobSortingTypes.TITLE, viewValue: 'by title'},
    {value: JobSortingTypes.AUTHOR, viewValue: 'by author'},
    {value: JobSortingTypes.STATUS, viewValue: 'by status'},
  ],
  results: [],
  params: {limit: DEFAULT_PAGINATED_STATE.limit, offset: DEFAULT_PAGINATED_STATE.offset},
  jobAuthors: []
}, DEFAULT_PAGINATED_STATE);


@State<ViewJobListPageStateModel>({
  name: 'ViewJobListPage',
  defaults: DEFAULT_COMPANY_PROFILE_PAGE_STATE,
})
export class ViewJobListPageState extends BaseBlockablePageState {
  @Selector()
  static count(state: ViewJobListPageStateModel): number {
    return state.count;
  }

  @Selector()
  static pageSize(state: ViewJobListPageStateModel): number {
    return state.pageSize;
  }

  @Selector()
  static pageSizeOptions(state: ViewJobListPageStateModel): Array<number> {
    return state.pageSizeOptions;
  }

  @Selector()
  static results(state: ViewJobListPageStateModel): Array<any> {
    return state.results;
  }

  @Selector()
  static jobAuthors(state: ViewJobListPageStateModel): Array<any> {
    return state.jobAuthors;
  }

  @Selector()
  static jobSortingFilters(state: ViewJobListPageStateModel): SortingFilter[] {
    return state.jobSortingFilter;
  }

  constructor(private jobService: JobService,
              private companyService: CompanyService) {
    super();
  }

  @Action(ViewJobListPageActions.LoadJobsData)
  loadJobsData(ctx: StateContext<ViewJobListPageStateModel>,
               {params}: ViewJobListPageActions.LoadJobsData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getJobs(params).pipe(
      tap((result) => {
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
          ...DEFAULT_PAGINATED_STATE,
          status: 'error',
          errors: error.error,
          results: [],
        }));
      }),
    );
  }

  @Action(ViewJobListPageActions.DeleteJob)
  deleteJob(ctx: StateContext<ViewJobListPageStateModel>, {jobId}) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.deleteJob(jobId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: `The job was deleted`,
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
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

  @Action(ViewJobListPageActions.DeleteJobList)
  deleteJobList(ctx: StateContext<ViewJobListPageStateModel>, {jobIds}) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.deleteJobList(jobIds).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: `The job's were deleted`,
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
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

  @Action(ViewJobListPageActions.DownloadJobList)
  downloadJobList(ctx: StateContext<ViewJobListPageStateModel>, {jobIds}) {
    ctx.patchState({
      status: 'pending',
    });
    return this.jobService.downloadJobList(jobIds).pipe(
      tap((responseBlob: Blob) => {
        const file = new File([responseBlob], `Job_Postings_${moment().format('L')}.csv`, {type: 'text/csv'});
        saveAs(file);
        return ctx.patchState({
          status: 'done',
          errors: null,
        });
      }),
      catchError(error => {
        return of(ctx.patchState({
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }

  @Action(ViewJobListPageActions.RestoreJob)
  restoreJob(ctx: StateContext<ViewJobListPageStateModel>, {jobId}) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.restoreJob(jobId).pipe(
      tap((jobItem: JobItem) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: `Job posting ${jobItem.title} has been restored successfully in the Draft status`,
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
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

  @Action(ViewJobListPageActions.UpdateParams)
  updateParams(ctx, {params, changeType}: ViewJobListPageActions.UpdateParams) {
    const state = ctx.getState();
    const newParams = {...state.params, ...GridViewHelper.prepareNewParams(params, changeType)};
    ctx.patchState({
      params: newParams
    });
    return ctx.dispatch(new ViewJobListPageActions.LoadJobsData(newParams));
  }

  @Action(ViewJobListPageActions.RemoveParams)
  removeParams(ctx, {paramsToDelete}: ViewJobListPageActions.RemoveParams) {
    const state = ctx.getState();
    const newParams = GridViewHelper.clearStateParams(state.params, paramsToDelete);
    return ctx.patchState({
      params: newParams
    });
  }

  @Action(ViewJobListPageActions.LoadJobsAuthorsData)
  loadJobAuthorsData(ctx: StateContext<ViewJobListPageStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyService.getJobAuthors().pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          jobAuthors: result.results,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          jobAuthors: [],
        }));
      }),
    );
  }
}
