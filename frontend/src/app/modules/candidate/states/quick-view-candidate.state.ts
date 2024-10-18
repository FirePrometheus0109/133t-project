import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { QuickViewCandidateActions } from '../actions';
import { CandidateItem } from '../models/candidate-item.model';
import { CandidateService } from '../services/candidate.service';


export class QuickViewCandidateStateModel extends BasePaginatedPageStateModel {
  results: Array<CandidateItem>;
  ordering: string;
}


export const DEFAULT_QUICK_VIEW_CANDIDATE_PAGE_STATE = Object.assign(DEFAULT_PAGINATED_STATE, {
  limit: 1,
  ordering: ''
});


@State<QuickViewCandidateStateModel>({
  name: 'QuickViewCandidateState',
  defaults: DEFAULT_QUICK_VIEW_CANDIDATE_PAGE_STATE,
})
export class QuickViewCandidateState extends BaseBlockablePageState {
  @Selector()
  static count(state: QuickViewCandidateStateModel): number {
    return state.count;
  }

  @Selector()
  static currentCandidate(state: QuickViewCandidateStateModel): CandidateItem {
    return state.results[0];
  }

  @Selector()
  static currentSortingField(state: QuickViewCandidateStateModel): string {
    return state.ordering;
  }

  @Selector()
  static offset(state: QuickViewCandidateStateModel): number {
    return state.offset;
  }

  @Selector()
  static next(state: QuickViewCandidateStateModel): any {
    return state.next;
  }

  @Selector()
  static previous(state: QuickViewCandidateStateModel): any {
    return state.previous;
  }

  constructor(private candidateService: CandidateService) {
    super();
  }

  @Action(QuickViewCandidateActions.LoadCandidateData)
  loadCandidateData(ctx, {params}: QuickViewCandidateActions.LoadCandidateData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
      ...params
    });
    return this.candidateService.getCandidateForQuickView(params).pipe(
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
          status: 'error',
          errors: error.error,
          count: 0,
          next: null,
          previous: null,
          results: [],
        }));
      }),
    );
  }

  @Action(QuickViewCandidateActions.ChangeCandidate)
  changeCandidate(ctx, {params}: QuickViewCandidateActions.ChangeCandidate) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return ctx.dispatch(new QuickViewCandidateActions.LoadCandidateData(params));
  }
}
