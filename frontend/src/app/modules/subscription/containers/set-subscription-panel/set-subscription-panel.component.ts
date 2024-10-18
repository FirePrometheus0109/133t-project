import { Component } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { AuthState } from 'src/app/modules/auth/states/auth.state';
import { StatesStatuses } from 'src/app/modules/shared/enums/states-statuses';
import { DateTimeHelper } from 'src/app/modules/shared/helpers/date-time.helper';
import { ConfirmationDialogService } from 'src/app/modules/shared/services/confirmation-dialog.service';
import { ManageSubsctiptionActions, SetSubscriptionActions } from '../../actions';
import { SetSubscriptionMessageHelper } from '../../helper/set-subsctiption-message.helper';
import { SubscriptionModel } from '../../models/subsctiption-plan.model';
import { SetSubscriptionState, SetSubscriptionStateModel } from '../../states/set-subscription.state';


@Component({
  selector: 'app-set-subscription-panel',
  templateUrl: './set-subscription-panel.component.html',
  styleUrls: ['./set-subscription-panel.component.scss']
})
export class SetSubscriptionPanelComponent {

  @Select(SetSubscriptionState.isActivePlanSelected) isActivePlanSelected$: Observable<number>;
  @Select(SetSubscriptionState.selectedPlan) selectedPlan$: Observable<SubscriptionModel>;
  @Select(SetSubscriptionState.activePlan) activePlan$: Observable<SubscriptionModel>;
  @Select(SetSubscriptionState.isLast) isLast$: Observable<boolean>;
  @Select(SetSubscriptionState.isFirst) isFirst$: Observable<boolean>;

  constructor(private store: Store, private dialog: ConfirmationDialogService) {
  }

  upvoteSubscription() {
    this.store.dispatch(new SetSubscriptionActions.UpvoteSubscription());
  }

  downvoteSubscription() {
    this.store.dispatch(new SetSubscriptionActions.DownvoteSubscription());
  }

  backToPackages() {
    this.store.dispatch(new SetSubscriptionActions.ReturnToPlans());
  }

  goToPaymentDetails() {
    this.store.dispatch(new SetSubscriptionActions.GoToPaymentDetails());
  }

  processPayment() {
    const selectedPlan = this.store.selectSnapshot(SetSubscriptionState.selectedPlan);
    const activePlan = this.activePlan;
    const company = this.store.selectSnapshot(AuthState.user).company;
    const isBillingCircleOver = !DateTimeHelper.isFuture(company.subscription.date_end);
    const isSelectedPlanCheaper = +selectedPlan.price < +activePlan.plan.price;
    const isAlreadyPurchased = activePlan.next_subscription;

    if (isAlreadyPurchased) {
      return this.dialog.openSimplifiedConfirmationDialog
      (SetSubscriptionMessageHelper.alreadyPurchasedSubscription(activePlan.next_subscription));
    }

    if (!selectedPlan.price) {
      return this.dialog.openSimplifiedConfirmationDialog(SetSubscriptionMessageHelper.starterPackageMessage,
        this.purchaseSubscription.bind(this, selectedPlan.id));
    }

    if (!company.is_billing_info_provided) {
      return this.goToPaymentDetails();
    }

    if (isBillingCircleOver) {
      return this.dialog.openSimplifiedConfirmationDialog(SetSubscriptionMessageHelper.confirmPaymentWithSavedCardMessage,
        this.purchaseSubscription.bind(this, selectedPlan.id));
    }

    if (!isSelectedPlanCheaper) {
      return this.dialog.openSimplifiedConfirmationDialog(SetSubscriptionMessageHelper.confirmPaymentWithSavedCardMessage,
        this.purchaseSubscription.bind(this, selectedPlan.id));
    }
    return this.dialog.openSimplifiedConfirmationDialog(SetSubscriptionMessageHelper.cheaperPurchaseMessage(activePlan, selectedPlan.name),
      this.purchaseSubscription.bind(this, selectedPlan.id));
  }

  getUntilDate() {
    return DateTimeHelper.getDate(this.activePlan.date_end.toString());
  }

  public get isAllPlansPassed() {
    return this.store.selectSnapshot(SetSubscriptionState.currentIndex) >
      this.store.selectSnapshot(SetSubscriptionState.allPlansLength) - 1;
  }

  private purchaseSubscription(planId: number) {
    this.store.dispatch(new SetSubscriptionActions.PurchaseSubscription(planId)).subscribe(result => {
      const currentState: SetSubscriptionStateModel = result.SetSubscriptionState;
      const planName = currentState.activePlan.next_subscription ? currentState.activePlan.next_subscription.plan.name :
        currentState.selectedPlan.name;
      if (currentState.status === StatesStatuses.DONE) {
        this.dialog.openSimplifiedConfirmationDialog(SetSubscriptionMessageHelper.successPurchaseMessage(planName));
        return this.store.dispatch(new ManageSubsctiptionActions.PaymentHistory());
      }
    });
  }

  private get activePlan() {
    return this.store.selectSnapshot(SetSubscriptionState.activePlan);
  }
}
