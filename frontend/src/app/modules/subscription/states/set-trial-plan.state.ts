import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { AuthActions } from '../../auth/actions';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { BasePaginatedPageStateModel, DEFAULT_PAGINATED_STATE } from '../../shared/states/base-paginated.state';
import { SetTrialPlanActions } from '../actions';
import { SubscriptionModel, SubscriptionPlan } from '../models/subsctiption-plan.model';
import { SubscriptionService } from '../services/subsctiption.service';


export class SetTrialPlanStateModel extends BasePaginatedPageStateModel {
  results: Array<SubscriptionPlan>;
  trialResult: any;
}


export const DEFAULT_SET_TRIAl_PAGE_STATE = Object.assign(DEFAULT_PAGINATED_STATE, {
  trialResult: ''
});


@State<SetTrialPlanStateModel>({
  name: 'SetTrialPlanState',
  defaults: DEFAULT_SET_TRIAl_PAGE_STATE
})
export class SetTrialPlanState {
  @Selector()
  static availablePlans(state: SetTrialPlanStateModel) {
    return state.results;
  }

  @Selector()
  static firstPlan(state: SetTrialPlanStateModel) {
    return state.results[0];
  }

  @Selector()
  static trialSuccess(state: SetTrialPlanStateModel) {
    return state.trialResult;
  }

  constructor(private service: SubscriptionService) {
  }

  @Action(SetTrialPlanActions.LoadAvailablePlans)
  loadAvailablePlans(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.service.getTrialPlans().pipe(
      tap((result: PaginatedData) => {
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

  @Action(SetTrialPlanActions.PurchaseTrialPackage)
  purchaseTrialPackage(ctx, {id}: SetTrialPlanActions.PurchaseTrialPackage) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.service.setTrial(id).pipe(
      tap((data: SubscriptionModel) => {
        state = ctx.getState();
        ctx.dispatch(new AuthActions.UpdateSubsctiption(data));
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          trialResult: data,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          trialResult: null,
        }));
      }),
    );
  }

}
