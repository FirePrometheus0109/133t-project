import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { AutoApplyListActions } from '../actions';
import { AutoApplyService } from '../services/auto-apply.service';


class AutoApplyListStateModel {
  status: string;
  errors: object;
  autoApplyList: Array<any>;
}


export const DEFAULT_AUTO_APPLY_LIST_STATE = {
  status: '',
  errors: null,
  autoApplyList: [],
};


@State<AutoApplyListStateModel>({
  name: 'AutoApplyList',
  defaults: DEFAULT_AUTO_APPLY_LIST_STATE
})
export class AutoApplyListState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static autoApplyList(state: any) {
    return state.autoApplyList;
  }

  constructor(private autoApplyService: AutoApplyService) {
  }

  @Action(AutoApplyListActions.LoadAutoApplyList)
  loadAutoApplyList(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.getAutoApplyList().pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          autoApplyList: result['results'],
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          autoApplyList: [],
        }));
      })
    );
  }

  @Action(AutoApplyListActions.DeleteAutoApplyItem)
  deleteAutoApplyItem(ctx, {autoApplyId}: AutoApplyListActions.DeleteAutoApplyItem) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.autoApplyService.deleteAutoApplyItem(autoApplyId).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new AutoApplyListActions.LoadAutoApplyList());
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
