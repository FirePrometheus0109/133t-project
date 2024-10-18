import { Component, OnInit } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { NavigationService } from 'src/app/modules/core/services/navigation.service';
import { StatesStatuses } from 'src/app/modules/shared/enums/states-statuses';
import { ConfirmationDialogService } from 'src/app/modules/shared/services/confirmation-dialog.service';
import { AuthState } from '../../../auth/states/auth.state';
import { ErrorService } from '../../../core/services/error.service';
import { ManageSubsctiptionActions, SetSubscriptionActions } from '../../actions';
import { SetSubscriptionMessageHelper } from '../../helper/set-subsctiption-message.helper';
import { PaymentHistoryItem, SubscriptionModel } from '../../models/subsctiption-plan.model';
import { ManageSubsctiptionState } from '../../states/manage-subscription.service';
import { SetSubscriptionState } from '../../states/set-subscription.state';


@Component({
  selector: 'app-manage-subscription',
  templateUrl: './manage-subscription.component.html',
  styleUrls: ['./manage-subscription.component.css']
})
export class ManageSubscriptionComponent implements OnInit {
  @Select(SetSubscriptionState.activePlan) activePlan$: Observable<SubscriptionModel>;
  @Select(ManageSubsctiptionState.paymentHistory) paymentHistory$: Observable<Array<PaymentHistoryItem>>;

  constructor(private store: Store,
              private dialog: ConfirmationDialogService,
              private navigationService: NavigationService,
              private errorService: ErrorService) {
  }

  ngOnInit() {
    if (!this.store.selectSnapshot(SetSubscriptionState.activePlan)) {
      this.store.dispatch(new SetSubscriptionActions.LoadCurrentPlan());
    }
  }

  onUnsubscribe() {
    const plan = this.store.selectSnapshot(SetSubscriptionState.activePlan);
    this.store.dispatch(new ManageSubsctiptionActions.Unsubscribe(plan)).subscribe(_ =>
      this.dialog.openSimplifiedConfirmationDialog(
        SetSubscriptionMessageHelper.successUnsubscription(plan.plan.name))
    );
  }

  onCancel() {
    const plan = this.store.selectSnapshot(SetSubscriptionState.activePlan).next_subscription;
    forkJoin([this.store.dispatch(new SetSubscriptionActions.CancelNextSubscription()),
      this.store.dispatch(new ManageSubsctiptionActions.Unsubscribe(plan))]).subscribe(_ =>
      this.dialog.openSimplifiedConfirmationDialog(
        SetSubscriptionMessageHelper.successUnsubscription(plan.plan.name))
    );
  }

  processRenew() {
    const activePlan = this.store.selectSnapshot(SetSubscriptionState.activePlan);
    if (!this.store.selectSnapshot(AuthState.user).company.is_billing_info_provided) {
      this.store.dispatch(new SetSubscriptionActions.GoToPaymentDetails());
    } else {
      return this.dialog.openSimplifiedConfirmationDialog(SetSubscriptionMessageHelper.confirmPaymentWithSavedCardMessage,
        this.purchaseSubscription.bind(this, activePlan.plan.id));
    }
  }

  changeBillingData() {
    this.navigationService.goToChangeBillingDataPage();
  }

  private purchaseSubscription(planId: number) {
    this.store.dispatch(new SetSubscriptionActions.PurchaseSubscription(planId)).subscribe(result => {
      const currentState = result.SetSubscriptionState;
      if (currentState.status === StatesStatuses.DONE) {
        this.dialog.openSimplifiedConfirmationDialog(SetSubscriptionMessageHelper.successPurchaseMessage
        (currentState.selectedPlan.name));
      }
    });
  }
}
