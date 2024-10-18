import { Action, Selector, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { CandidatesQuickListActions } from '../actions';
import { CandidateQuickListItem } from '../models/candidate-quick-list.model';
import { CandidateService } from '../services/candidate.service';


export class CandidatesQuickListStateModel {
  status: string;
  errors: object;
  candidatesQuickList: CandidateQuickListItem[];
  params: object;
}


export const DEFAULT_CANDIDATES_QUICKLIST_STATE = {
  status: '',
  errors: null,
  candidatesQuickList: [],
  params: {}
};


@State<CandidatesQuickListStateModel>({
  name: 'CandidatesQuickListState',
  defaults: DEFAULT_CANDIDATES_QUICKLIST_STATE
})
export class CandidatesQuickListState {
  @Selector()
  static candidatesQuickList(state: CandidatesQuickListStateModel): CandidateQuickListItem[] {
    return state.candidatesQuickList;
  }

  @Selector()
  static params(state: CandidatesQuickListStateModel): object {
    return state.params;
  }

  constructor(private candidateService: CandidateService) {
  }

  @Action(CandidatesQuickListActions.UpdateQuickListParams)
  updateQuickListParams(ctx: StateContext<CandidatesQuickListStateModel>,
                        {params}: CandidatesQuickListActions.UpdateQuickListParams) {
    let state = ctx.getState();
    const updatedParams = Object.assign(state.params, params);
    for (const [key, value] of Object.entries(updatedParams)) {
      if (!value) {
        delete updatedParams[key];
      }
    }
    ctx.setState({
      ...state,
      params: updatedParams
    });
    state = ctx.getState();
    return ctx.dispatch(new CandidatesQuickListActions.GetCandidatesQuickList(state.params));
  }

  @Action(CandidatesQuickListActions.GetCandidatesQuickList)
  getCandidatesQuickList(ctx: StateContext<CandidatesQuickListStateModel>,
                         {params}: CandidatesQuickListActions.GetCandidatesQuickList) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.candidateService.getCandidatesQuickList(params).pipe(
      tap((result: CandidateQuickListItem[]) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          candidatesQuickList: result,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          candidatesQuickList: [],
        }));
      }),
    );
  }
}
