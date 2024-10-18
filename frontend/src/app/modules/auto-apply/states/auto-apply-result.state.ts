import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { JobService } from '../../company/services/job.service';
import { CoreActions } from '../../core/actions';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { AutoApplyResultActions } from '../actions';
import { AutoApply, Job } from '../models/auto-apply.model';
import { AutoApplyService } from '../services/auto-apply.service';


class AutoApplyResultStateModel {
  title: string;
  status: string;
  errors: object;
  query_params: any;
  autoApply: AutoApply;
  autoApplyResult: Array<Job>;
  autoApplyResultApplied: Array<Job>;
  autoApplyResultNeedReview: Array<Job>;
  autoApplyResultNewJobs: Array<Job>;
  selectedJobDetail: object;
}


export const DEFAULT_AUTO_APPLY_RESULT_STATE = {
  title: '',
  status: '',
  errors: null,
  query_params: null,
  autoApply: null,
  autoApplyResult: [],
  autoApplyResultApplied: [],
  autoApplyResultNeedReview: [],
  autoApplyResultNewJobs: [],
  selectedJobDetail: null,
};


@State<AutoApplyResultStateModel>({
  name: 'AutoApplyResult',
  defaults: DEFAULT_AUTO_APPLY_RESULT_STATE
})
export class AutoApplyResultState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static autoApply(state: any) {
    return state.autoApply;
  }

  @Selector()
  static autoApplyResult(state: any) {
    return state.autoApplyResult;
  }

  @Selector()
  static autoApplyResultApplied(state: any) {
    return state.autoApplyResultApplied;
  }

  @Selector()
  static autoApplyResultNeedReview(state: any) {
    return state.autoApplyResultNeedReview;
  }

  @Selector()
  static autoApplyResultNewJobs(state: any) {
    return state.autoApplyResultNewJobs;
  }

  @Selector()
  static selectedJobDetail(state: any) {
    return state.selectedJobDetail;
  }

  @Selector()
  static queryParams(state: any) {
    return state.query_params;
  }

  constructor(private autoApplyService: AutoApplyService, private jobService: JobService) {
  }

  @Action(AutoApplyResultActions.LoadAutoApply)
  loadAutoApply(ctx, {autoApplyId}: AutoApplyResultActions.LoadAutoApply) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.getAutoApply(autoApplyId).pipe(
      tap((result: AutoApply) => {
        state = ctx.getState();
        const transformedQueryParams = this.autoApplyService.getQueryParamsForResult({
          ...this.autoApplyService.getQueryParams(result.query_params),
          location: result.location
        });
        ctx.setState({
          ...state,
          query_params: transformedQueryParams,
          status: 'done',
          errors: null,
          autoApply: result,
        });
        return ctx.dispatch(new AutoApplyResultActions.GetAutoApplyResult(result.id));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          autoApply: null,
        }));
      })
    );
  }

  @Action(AutoApplyResultActions.GetAutoApplyResult)
  getAutoApplyResult(ctx, {autoApplyId}: AutoApplyResultActions.GetAutoApplyResult) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.getAutoApplyResult(autoApplyId).pipe(
      tap((result) => {
        state = ctx.getState();
        const dividedResult = this.autoApplyService.divideAutoApplyResult(result.results);
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          autoApplyResult: result.results,
          autoApplyResultApplied: dividedResult.applied,
          autoApplyResultNeedReview: dividedResult.need_review,
          autoApplyResultNewJobs: dividedResult.new_jobs,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          autoApplyResult: [],
          autoApplyResultApplied: [],
          autoApplyResultNeedReview: [],
          autoApplyResultNewJobs: [],
        }));
      })
    );
  }

  @Action(AutoApplyResultActions.StopAutoApply)
  stopAutoApply(ctx, {autoApplyId}: AutoApplyResultActions.StopAutoApply) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.stopAutoApply(autoApplyId).pipe(
      tap((stoppedAutoApply) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          autoApply: stoppedAutoApply,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }

  @Action(AutoApplyResultActions.RestartAutoApply)
  restartAutoApply(ctx, {autoApplyId}: AutoApplyResultActions.RestartAutoApply) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.restartAutoApply(autoApplyId).pipe(
      tap((restartedAutoApply) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          autoApply: restartedAutoApply,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }

  @Action(AutoApplyResultActions.ApplyForNewJob)
  applyForNewJob(ctx, {autoApplyId, jobId}: AutoApplyResultActions.ApplyForNewJob) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.applyForNewJob(autoApplyId, jobId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new AutoApplyResultActions.GetAutoApplyResult(autoApplyId));
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You\'ve applied for the job',
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
      })
    );
  }

  @Action(AutoApplyResultActions.GetSelectedJob)
  getSelectedJobForModal(ctx, {jobId}: AutoApplyResultActions.GetSelectedJob) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.jobService.getJobById(jobId).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          selectedJobDetail: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          selectedJobDetail: [],
        }));
      })
    );
  }

  @Action(AutoApplyResultActions.SetCoverLetterForApply)
  setCoverLetterForApply(ctx, {autoApplyId, jobId, coverLetterData}: AutoApplyResultActions.SetCoverLetterForApply) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.setCoverLetterForApply(autoApplyId, jobId, coverLetterData).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new AutoApplyResultActions.GetAutoApplyResult(autoApplyId));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }
}
