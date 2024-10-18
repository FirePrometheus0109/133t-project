import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { JobService } from '../../company/services/job.service';
import { Answer } from '../../survey/models/answer.model';
import { JobSeekerAppliedListActions } from '../actions';


class ViewAppliedJobListPageStateModel {
  status: string;
  errors: object;
  answersForJob: Array<Answer>;
}


export const DEFAULT_APPLIED_JOBS_PAGE_STATE = {
  status: '',
  errors: null,
  answersForJob: [],
};


@State<ViewAppliedJobListPageStateModel>({
  name: 'ViewAppliedJobListPage',
  defaults: DEFAULT_APPLIED_JOBS_PAGE_STATE,
})
export class ViewAppliedJobListPageState {
  @Selector()
  static answersForJob(state: any) {
    return state.answersForJob;
  }

  constructor(private jobService: JobService) {
  }

  @Action(JobSeekerAppliedListActions.LoadAnswersForJob)
  loadAnswersForJob(ctx: StateContext<ViewAppliedJobListPageStateModel>,
                    {jobId, jsId}: JobSeekerAppliedListActions.LoadAnswersForJob) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.jobService.getCandidateAnswer(jobId, jsId).pipe(
      tap((result: Array<Answer>) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          answersForJob: result
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          answersForJob: []
        }));
      }),
    );
  }
}
