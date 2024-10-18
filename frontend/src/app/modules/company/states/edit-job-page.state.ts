import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { CoreActions } from '../../core/actions';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { SurveyListActions } from '../../survey/actions';
import { EditJobPageActions } from '../actions';
import { JobService } from '../services/job.service';


export class EditJobPageStateModel {
  status: string;
  errors: object;
  initialData: object;
}


export const DEFAULT_EDIT_JOB_PAGE_STATE = {
  status: '',
  errors: null,
  initialData: null,
};


@State<EditJobPageStateModel>({
  name: 'EditJobPageState',
  defaults: DEFAULT_EDIT_JOB_PAGE_STATE,
})
export class EditJobPageState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static initialData(state: any) {
    return state.initialData;
  }

  constructor(private jobService: JobService) {
  }

  @Action(EditJobPageActions.LoadInitialData)
  loadInitialData(ctx, {id}: EditJobPageActions.LoadInitialData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getJobById(id).pipe(
      tap((result) => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          initialData: result,
        });
        ctx.dispatch(new SurveyListActions.SetCurrentSurvey(null));
        ctx.dispatch(new SurveyListActions.SetJobEditMode(true));
        ctx.dispatch(new SurveyListActions.UpdateSurveyForJobEdit(result['questions']));
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          initialData: null,
        }));
      }),
    );
  }

  @Action(EditJobPageActions.UpdateJob)
  updateJobPosting(ctx, {id, data}: EditJobPageActions.UpdateJob) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.updateJob(id, data).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        return ctx.dispatch(new CoreActions.SnackbarOpen({
          message: 'You have successfully updated job.',
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
