import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { AuthActions } from '../../auth/actions';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { PaginatedData } from '../../shared/models/paginated-data.model';
import { SetSubscriptionActions } from '../actions';
import { SubscriptionModel, SubscriptionPlan } from '../models/subsctiption-plan.model';
import { SubscriptionService } from '../services/subsctiption.service';


export class SetSubscriptionStateModel {
  status: string;
  errors: object;
  activePlan: SubscriptionModel;
  allPlans: Array<SubscriptionPlan>;
  selectedPlan: SubscriptionPlan;
  purchasedPlan: SubscriptionPlan;
  currentIndex: number;
}


export const DEFAULT_SUBSCRIPTION_STATE = {
  status: '',
  errors: null,
  activePlan: null,
  selectedPlan: null,
  purchasedPlan: null,
  currentIndex: null,
  allPlans: [],
};


@State<SetSubscriptionStateModel>({
  name: 'SetSubscriptionState',
  defaults: DEFAULT_SUBSCRIPTION_STATE
})
export class SetSubscriptionState {
  @Selector()
  static isActivePlanSelected(state: SetSubscriptionStateModel): boolean {
    return state.selectedPlan.id === state.activePlan.plan.id;
  }

  @Selector()
  static isFirst(state: SetSubscriptionStateModel) {
    return state.allPlans.findIndex(plan => plan.id === state.selectedPlan.id) === 0;
  }

  @Selector()
  static isLast(state: SetSubscriptionStateModel) {
    return state.allPlans.findIndex(plan =>
      plan.id === state.selectedPlan.id) === state.allPlans.length - 1;
  }

  @Selector()
  static selectedPlan(state: SetSubscriptionStateModel) {
    return state.selectedPlan;
  }

  @Selector()
  static activePlan(state: SetSubscriptionStateModel) {
    return state.activePlan;
  }

  @Selector()
  static purchasedPlan(state: SetSubscriptionStateModel) {
    return state.purchasedPlan;
  }

  @Selector()
  static currentIndex(state: SetSubscriptionStateModel) {
    return state.currentIndex;
  }

  @Selector()
  static allPlansLength(state: SetSubscriptionStateModel) {
    return state.allPlans.length;
  }

  constructor(private service: SubscriptionService,
              private navigationService: NavigationService) {
  }

  @Action(SetSubscriptionActions.LoadAllPlans)
  loadAllPlans(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.service.getAvailablePlan().pipe(
      tap((result: PaginatedData) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          allPlans: result.results
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          allPlans: []
        }));
      }),
    );
  }

  @Action(SetSubscriptionActions.UpdatePaymentData)
  updatePaymentData(ctx, {data}: SetSubscriptionActions.UpdatePaymentData) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    ctx.dispatch(new CoreActions.ShowGlobalLoader());
    return this.service.updateBillingData(data).pipe(
      tap(_ => {
        state = ctx.getState();
        ctx.dispatch(new AuthActions.UpdateBillingInformation());
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
      }),
    );
  }

  @Action(SetSubscriptionActions.PurchaseSubscription)
  purchaseSubscription(ctx, {plan}: SetSubscriptionActions.PurchaseSubscription) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    ctx.dispatch(new CoreActions.ShowGlobalLoader());
    return this.service.purchaseSubscription(plan).pipe(
      tap((result: SubscriptionModel) => {
        state = ctx.getState();
        ctx.dispatch(new AuthActions.UpdateSubsctiption(result));
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          activePlan: result,
          selectedPlan: result.next_subscription ? result.next_subscription.plan : result.plan,
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

  @Action(SetSubscriptionActions.LoadCurrentPlan)
  loadCurrentPlan(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.service.getActivePlan().pipe(
      tap((result: SubscriptionModel) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          activePlan: result,
          selectedPlan: result.plan,
          currentIndex: state.allPlans.findIndex(plan => plan.id === result.plan.id)
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          activePlan: null,
          selectedPlan: null
        }));
      }),
    );
  }

  @Action(SetSubscriptionActions.GoToPaymentDetails)
  goToPaymentDetails(ctx) {
    const state = ctx.getState();
    ctx.setState({
      ...state,
      purchasedPlan: state.selectedPlan
    });
    return this.navigationService.goToPaymentPage();
  }

  @Action(SetSubscriptionActions.UpvoteSubscription)
  upvoteSubscription(ctx) {
    const state = ctx.getState();

    if (!SetSubscriptionState.isLast(state)) {
      const currentIndex = state.allPlans.findIndex(plan => plan.id === state.selectedPlan.id);
      return ctx.setState({
        ...state,
        selectedPlan: state.allPlans[currentIndex + 1],
        currentIndex: currentIndex + 1
      });
    } else {
      return ctx.setState({
        ...state,
        currentIndex: state.currentIndex + 1
      });
    }
  }

  @Action(SetSubscriptionActions.DownvoteSubscription)
  downSubscription(ctx) {
    const state = ctx.getState();

    if (!SetSubscriptionState.isFirst(state)) {
      const currentIndex = state.allPlans.findIndex(plan => plan.id === state.selectedPlan.id);
      return ctx.setState({
        ...state,
        selectedPlan: state.allPlans[currentIndex - 1],
        currentIndex: currentIndex - 1
      });
    }
  }

  @Action(SetSubscriptionActions.CancelNextSubscription)
  cancelNextSubscription(ctx) {
    const state: SetSubscriptionStateModel = ctx.getState();
    const activePlan = state.activePlan;
    activePlan.next_subscription = null;
    return ctx.setState({
      ...state,
      activePlan: activePlan
    });
  }

  @Action(SetSubscriptionActions.SetFirstPlanSelected)
  setFirstPlanSelected(ctx) {
    const state = ctx.getState();
    const [defaultPlan] = state.allPlans;
    return ctx.setState({
      ...state,
      // set selectedPlan and activePlan like default from plans list when subscription was deleted
      selectedPlan: defaultPlan,
      activePlan: {plan: defaultPlan}
    });
  }

  @Action(SetSubscriptionActions.ReturnToPlans)
  returnToPlans(ctx) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      currentIndex: state.currentIndex - 1
    });
  }
}
