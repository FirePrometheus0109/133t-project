import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { ManageSubsctiptionActions } from '../actions';
import { PaymentHistoryItem } from '../models/subsctiption-plan.model';
import { SubscriptionService } from '../services/subsctiption.service';


export class ManageSubsctiptionStateModel {
  status: string;
  errors: object;
  paymentHistory: Array<PaymentHistoryItem>;
}


export const DEFAULT_MANAGE_SUBSCRIPTION_STATE = {
  status: '',
  errors: null,
  paymentHistory: []
};


@State<ManageSubsctiptionStateModel>({
  name: 'ManageSubsctiptionState',
  defaults: DEFAULT_MANAGE_SUBSCRIPTION_STATE
})
export class ManageSubsctiptionState {
  @Selector()
  static paymentHistory(state: ManageSubsctiptionStateModel) {
    return state.paymentHistory;
  }

  constructor(private service: SubscriptionService,
              private messageDialog: ConfirmationDialogService) {
  }

  @Action(ManageSubsctiptionActions.PaymentHistory)
  paymentHistory(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.service.getPaymentHistory().pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          paymentHistory: result
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          paymentHistory: []
        }));
      }),
    );
  }

  @Action(ManageSubsctiptionActions.Unsubscribe)
  unsubscribe(ctx, {subscription}: ManageSubsctiptionActions.Unsubscribe) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });

    return this.service.unsubscribeSubscription(subscription.id).pipe(
      tap(_ => {
        state = ctx.getState();
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
}
