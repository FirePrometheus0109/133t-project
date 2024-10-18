import { Action, Selector, State, Store } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { JobService } from '../../company/services/job.service';
import { CoreState } from '../../core/states/core.state';
import { ManualApplyActions } from '../actions';
import { ManualApplyMessageHelper } from '../helpers/manual-apply-validation-message.helper';
import { ManualApplyService } from '../services';


class ManualApplyStateModel {
  status: string;
  errors: object;
  jobData: object;
  applyResult: boolean;
  isApplyPossible: boolean;
  isReapplyPossible: boolean;
  validationMessage: string;
}


export const DEFAULT_MANUALAPPLY_STATE = {
  status: '',
  errors: null,
  jobData: null,
  applyResult: false,
  isApplyPossible: false,
  isReapplyPossible: false,
  validationMessage: ManualApplyMessageHelper.getInitialMessage(),
};


@State<ManualApplyStateModel>({
  name: 'ManualApply',
  defaults: DEFAULT_MANUALAPPLY_STATE
})
export class ManualApplyState {
  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static applyResult(state: any) {
    return state.applyResult;
  }

  @Selector()
  static jobData(state: any) {
    return state.jobData;
  }

  @Selector()
  static validationMessage(state: any) {
    return state.validationMessage;
  }

  @Selector()
  static isApplyPossible(state: any) {
    return state.isApplyPossible;
  }

  @Selector()
  static isReapplyPossible(state: any) {
    return state.isReapplyPossible;
  }

  constructor(private jsService: ManualApplyService,
              private jobService: JobService,
              private store: Store) {
  }

  @Action(ManualApplyActions.ManualApplyForJob)
  applyForJob(ctx, {jobId, coverLetterData}: ManualApplyActions.ManualApplyForJob) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.jsService.applyForJob(jobId, coverLetterData).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          applyResult: result['status']
        });
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

  @Action(ManualApplyActions.ReapplyForJob)
  reapplyForJob(ctx, {jobId, coverLetterData}: ManualApplyActions.ReapplyForJob) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.jobService.reapplyForJob(jobId, coverLetterData).pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          applyResult: result['status']
        });
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

  @Action(ManualApplyActions.ChangeManualApplyPossibility)
  changeApplyPossibility(ctx, {jobData}: ManualApplyActions.ChangeManualApplyPossibility) {
    const state = ctx.getState();
    const jobDataIds = this.store.selectSnapshot(CoreState.appliedJobDataIds);
    const result = jobData.is_clearance_match && jobData.is_education_match
      && !jobDataIds.includes(jobData.id);
    const isReapplyPossible = jobData.is_clearance_match && jobData.is_education_match
      && jobDataIds.includes(jobData.id);

    if (!jobData.is_clearance_match) {
      ctx.dispatch(new ManualApplyActions.ChangeManualApplyValidationMessage
      (ManualApplyMessageHelper.addClearanceError()));
    }

    if (!jobData.is_education_match) {
      ctx.dispatch(new ManualApplyActions.ChangeManualApplyValidationMessage
      (ManualApplyMessageHelper.addEducationError()));
    }

    return ctx.setState({
      ...state,
      isApplyPossible: result,
      isReapplyPossible: isReapplyPossible,
    });
  }

  @Action(ManualApplyActions.ChangeManualApplyValidationMessage)
  changeValidationMessage(ctx, {message}: ManualApplyActions.ChangeManualApplyValidationMessage) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      validationMessage: state.validationMessage.concat(message),
    });
  }

  @Action(ManualApplyActions.ResetManualApplyState)
  resetManualApplyState(ctx) {
    return ctx.setState(DEFAULT_MANUALAPPLY_STATE);
  }
}
