import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Job } from '../../auto-apply/models/auto-apply.model';
import { CoreActions } from '../../core/actions';
import { ManualApplyService } from '../../manual-apply/services';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { ViewJobDetailsJSPageActions } from '../actions';
import { JobService } from '../services/job.service';


class ViewJobDetailsJsPageStateModel {
  status: string;
  errors: object;
  jobData: Job;
}


export const DEFAULT_JOB_DETAILS_PAGE_STATE = {
  status: '',
  errors: null,
  jobData: null,
};


@State<ViewJobDetailsJsPageStateModel>({
  name: 'ViewJobDetailsJsPageState',
  defaults: DEFAULT_JOB_DETAILS_PAGE_STATE,
})
export class ViewJobDetailsJsPageState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static jobData(state: any) {
    return state.jobData;
  }

  constructor(private jobService: JobService, private manualApplyService: ManualApplyService) {
  }

  @Action(ViewJobDetailsJSPageActions.LoadJobData)
  loadJobData(ctx, {jobId}: ViewJobDetailsJSPageActions.LoadJobData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getJobById(jobId).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          jobData: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          jobData: null,
        }));
      }),
    );
  }

  @Action(ViewJobDetailsJSPageActions.LoadPublicJobData)
  loadPublicJobData(ctx, {jobUid}: ViewJobDetailsJSPageActions.LoadPublicJobData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getPublicJobByUid(jobUid).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          jobData: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          jobData: null,
        }));
      }),
    );
  }

  @Action(ViewJobDetailsJSPageActions.ApplyForJob)
  applyForJob(ctx, {jobId}: ViewJobDetailsJSPageActions.ApplyForJob) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.manualApplyService.applyForJob(jobId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You\'ve successfully applied for the job',
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
}
