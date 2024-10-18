import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { CityModel, StateModel } from '../../shared/models/address.model';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { LocationFilterService } from '../../shared/services/location-filter.service';
import { AutoApplyEditActions, AutoApplyListActions } from '../actions';
import { AutoApply } from '../models/auto-apply.model';
import { AutoApplyService } from '../services/auto-apply.service';


class AutoApplyEditStateModel {
  id: number;
  title: string;
  status: string;
  autoApplyStatus: string;
  query_params: object;
  number: number;
  owner: number;
  errors: object;
  autoApplyResult: Array<any>;
  autoApplyJobsList: Array<any>;
  stopped_jobs: Array<any>;
  deleted_jobs: Array<any>;
  applied_jobs: Array<any>;
  selectedJobDetail: object;
  create_mode: boolean;
  initialSearch: string;
  initialLocation: CityModel | StateModel;
  changesOccurred: boolean;
}


export const DEFAULT_AUTO_APPLY_EDIT_STATE = {
  id: null,
  title: '',
  status: '',
  autoApplyStatus: '',
  query_params: {},
  number: null,
  owner: null,
  errors: null,
  autoApplyResult: [],
  autoApplyJobsList: [],
  stopped_jobs: [],
  deleted_jobs: [],
  applied_jobs: [],
  selectedJobDetail: {},
  create_mode: false,
  initialSearch: '',
  initialLocation: null,
  changesOccurred: false,
};


@State<AutoApplyEditStateModel>({
  name: 'AutoApplyEdit',
  defaults: DEFAULT_AUTO_APPLY_EDIT_STATE
})
export class AutoApplyEditState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static autoApplyResult(state: any) {
    return state.autoApplyResult;
  }

  @Selector()
  static autoApplyJobsList(state: any) {
    return state.autoApplyJobsList;
  }

  @Selector()
  static autoApplyJobsCount(state: any) {
    return state.autoApplyJobsList.length;
  }

  @Selector()
  static queryParams(state: any) {
    return state.query_params;
  }

  @Selector()
  static stoppedJobs(state: any) {
    return state.stopped_jobs;
  }

  @Selector()
  static deletedJobs(state: any) {
    return state.deleted_jobs;
  }

  @Selector()
  static editFormData(state: any) {
    return {
      title: state.title,
      number: state.number,
    };
  }

  @Selector()
  static searchFormData(state: any) {
    return state.query_params;
  }

  @Selector()
  static specifyNumber(state: any) {
    return state.number;
  }

  @Selector()
  static selectedJobDetail(state: any) {
    return state.selectedJobDetail;
  }

  @Selector()
  static autoApplyStatus(state: any) {
    return state.autoApplyStatus;
  }

  @Selector()
  static appliedJobs(state: any) {
    return state.applied_jobs;
  }

  @Selector()
  static createMode(state: any) {
    return state.create_mode;
  }

  @Selector()
  static changesOccurred(state: any): boolean {
    return state.changesOccurred;
  }

  constructor(private autoApplyService: AutoApplyService,
              private navigationService: NavigationService) {
  }

  @Action(AutoApplyEditActions.LoadAutoApply)
  loadAutoApplyEdit(ctx, {autoApplyId}: AutoApplyEditActions.LoadAutoApply) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.getAutoApply(autoApplyId).pipe(
      tap((result: AutoApply) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          id: result.id,
          title: result.title,
          query_params: {
            ...this.autoApplyService.getQueryParams(result.query_params),
            location: result.location
          },
          number: result.number,
          owner: result.owner,
          stopped_jobs: result.stopped_jobs,
          deleted_jobs: result.deleted_jobs,
          autoApplyStatus: result.status,
          status: 'done',
          errors: null,
          autoApplyResult: result.autoapply_result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          autoApplyResult: [],
        }));
      })
    );
  }

  @Action(AutoApplyEditActions.SetQueryParams)
  setQueryParams(ctx, {params}: AutoApplyEditActions.SetQueryParams) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    const queryParams = state.query_params;
    Object.assign(queryParams, params);
    state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      query_params: queryParams,
      changesOccurred: true
    });
    return ctx.dispatch(new AutoApplyEditActions.LoadAutoApplyJobsList());
  }

  @Action(AutoApplyEditActions.SetCreateMode)
  setCreateMode(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      create_mode: true,
    });
  }

  @Action(AutoApplyEditActions.CreateAutoApply)
  createAutoApply(ctx, {params}: AutoApplyEditActions.CreateAutoApply) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
      title: params.title,
      number: params.number,
    });
    params.query_params = this.autoApplyService.setQueryParams(params.query_params);
    return this.autoApplyService.createAutoApply(params).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          changesOccurred: false,
          status: 'done',
          errors: null,
        });
        return setTimeout(() => this.navigationService.goToAutoApplyListPage());
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

  @Action(AutoApplyEditActions.UpdateAutoApply)
  updateAutoApply(ctx, {params, autoApplyId}: AutoApplyEditActions.UpdateAutoApply) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
      title: params.title,
      number: params.number,
    });
    params.query_params = this.autoApplyService.setQueryParams(params.query_params);
    return this.autoApplyService.updateAutoApply(params, autoApplyId).pipe(
      tap(() => {
        state = ctx.getState();
        this.navigationService.goToAutoApplyListPage();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
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

  @Action(AutoApplyEditActions.LoadAutoApplyJobsList)
  loadJobsForAutoApply(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    let requestParams;
    state.query_params.hasOwnProperty('location') ?
      requestParams = LocationFilterService.autoApplyPrepareLocationData(state.query_params) :
      requestParams = state.query_params;
    return this.autoApplyService.getAutoApplyJobsList(requestParams).pipe(
      tap((result) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          autoApplyJobsList: result['results'],
        });
        return ctx.dispatch(new AutoApplyEditActions.SetAppliedJobs());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          autoApplyJobsList: [],
        }));
      })
    );
  }

  @Action(AutoApplyEditActions.LoadAutoApplyJobs)
  loadAutoApplyJobs(ctx, {autoApplyId}: AutoApplyEditActions.LoadAutoApplyJobs) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.getAutoApplyJobs(autoApplyId).pipe(
      tap((result) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          autoApplyJobsList: result['results'],
        });
        return ctx.dispatch(new AutoApplyEditActions.SetAppliedJobs());
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          autoApplyJobsList: [],
        }));
      })
    );
  }

  @Action(AutoApplyEditActions.GetSelectedJob)
  getSelectedJobForModal(ctx, {jobId}: AutoApplyEditActions.GetSelectedJob) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.getAutoApplyJobDetails(jobId).pipe(
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

  @Action(AutoApplyEditActions.SetDeletedJobs)
  setDeletedJobs(ctx, {deletedJobId}: AutoApplyEditActions.SetDeletedJobs) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    const stateDeletedJobs = state.deleted_jobs;
    stateDeletedJobs.push(deletedJobId);
    state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      deleted_jobs: stateDeletedJobs,
    });
    return ctx.dispatch(new AutoApplyEditActions.SetQueryParams({exclude: stateDeletedJobs}));
  }

  @Action(AutoApplyEditActions.SetStoppedJobs)
  setStoppedJobs(ctx, {jobIdToStop}: AutoApplyEditActions.SetStoppedJobs) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    const stateStoppedJobs = state.stopped_jobs;
    stateStoppedJobs.push(jobIdToStop);
    state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      stopped_jobs: stateStoppedJobs,
    });
    return ctx.dispatch(new AutoApplyEditActions.SetAppliedJobs());
  }

  @Action(AutoApplyEditActions.ReturnJobFromStopped)
  returnJobFromStopped(ctx, {stoppedJobId}: AutoApplyEditActions.ReturnJobFromStopped) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    let stateStoppedJobs = state.stopped_jobs;
    stateStoppedJobs = stateStoppedJobs.filter(item => item !== stoppedJobId);
    state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      stopped_jobs: stateStoppedJobs,
    });
    return ctx.dispatch(new AutoApplyEditActions.SetAppliedJobs());
  }

  @Action(AutoApplyEditActions.SetSpecifyNumber)
  setSpecifyNumber(ctx, {number}: AutoApplyEditActions.SetSpecifyNumber) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      number: number,
    });
    return ctx.dispatch(new AutoApplyEditActions.SetAppliedJobs());
  }

  @Action(AutoApplyEditActions.SetTitle)
  setTitle(ctx, {title}: AutoApplyEditActions.SetTitle) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      title: title,
      changesOccurred: true
    });
  }

  @Action(AutoApplyEditActions.SetAppliedJobs)
  setAppliedJobs(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    let result = [];
    const deletedJobs = state.deleted_jobs;
    const stoppedJobs = state.stopped_jobs;
    const specifyNumber = state.number;
    const jobList = state.autoApplyJobsList;
    jobList.forEach(item => {
      result.push(item.id);
    });
    result = result.filter((el) => !deletedJobs.includes(el));
    result = result.filter((el) => !stoppedJobs.includes(el));
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      applied_jobs: result.slice(0, specifyNumber),
    });
  }

  @Action(AutoApplyEditActions.StartAutoApply)
  startAutoApply(ctx, {autoApplyId, appliedJobs}: AutoApplyEditActions.StartAutoApply) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    return this.autoApplyService.startAutoApply(autoApplyId, appliedJobs).pipe(
      tap((result) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          autoApplyResult: result,
        });
        this.navigationService.goToAutoApplyListPage();
        ctx.dispatch(new AutoApplyListActions.LoadAutoApplyList());
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: `You have successfully started auto apply for ${appliedJobs.applied_jobs.length} jobs. Now you can study the results.`,
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
      }),
      catchError((error) => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          autoApplyResult: [],
        }));
      })
    );
  }

  @Action(AutoApplyEditActions.CleanAutoApplyData)
  cleanAutoApplyData(ctx) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      ...DEFAULT_AUTO_APPLY_EDIT_STATE,
      query_params: {}
    });
  }

  @Action(AutoApplyEditActions.CreateAutoApplyFromId)
  createAutoApplyFromId(ctx, {autoApplyId}: AutoApplyEditActions.CreateAutoApplyFromId) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    this.navigationService.goToAutoApplyCreatePage();
    return this.autoApplyService.getAutoApply(autoApplyId).pipe(
      tap((result: AutoApply) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          title: result.title,
          query_params: {
            ...this.autoApplyService.getQueryParams(result.query_params),
            location: result.location
          },
          number: result.number,
          status: 'done',
          errors: null,
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
}
