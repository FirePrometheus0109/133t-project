import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Job } from '../../auto-apply/models/auto-apply.model';
import { CompanyService } from '../../company/services/company.service';
import { AssignCandidateActions } from '../actions';
import { CandidateService } from '../services/candidate.service';


export class AssignCandidateStateModel {
  status: string;
  errors: object;
  jobData: Array<Job>;
  assignmentResult: object;
}


export const DEFAULT_ASSIGN_CANDIDATE_STATE = {
  status: '',
  errors: null,
  jobData: [],
  assignmentResult: null
};


@State<AssignCandidateStateModel>({
  name: 'AssignCandidateState',
  defaults: DEFAULT_ASSIGN_CANDIDATE_STATE
})
export class AssignCandidateState {
  @Selector()
  static assignmentResult(state: AssignCandidateStateModel) {
    return state.assignmentResult;
  }

  @Selector()
  static jobData(state: AssignCandidateStateModel) {
    return state.jobData;
  }

  constructor(private companyService: CompanyService,
              private candidateService: CandidateService) {
  }

  @Action(AssignCandidateActions.ResetAssignmentWindow)
  resetAssignmentWindow(ctx: StateContext<AssignCandidateStateModel>) {
    ctx.setState(DEFAULT_ASSIGN_CANDIDATE_STATE);
  }

  @Action(AssignCandidateActions.AssignCandidate)
  assignCandidate(ctx: StateContext<AssignCandidateStateModel>,
                  {users, jobs}: AssignCandidateActions.AssignCandidate) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    const userIds = users.map(user => user.id);
    const jobIds = jobs.map(job => job.id);
    return this.candidateService.assignCandidate(userIds, jobIds).pipe(
      tap((data) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          assignmentResult: data,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          assignmentResult: null,
        }));
      }),
    );
  }

  @Action(AssignCandidateActions.LoadInitialData)
  loadInitialData(ctx: StateContext<AssignCandidateStateModel>) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyService.getActiveCompanyJob().pipe(
      tap((data) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          jobData: data.results,
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
}
