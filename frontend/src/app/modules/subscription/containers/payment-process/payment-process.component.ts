import { Component } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from 'src/app/modules/core/services/navigation.service';
import { ConfirmationDialogService } from 'src/app/modules/shared/services/confirmation-dialog.service';
import { SetSubscriptionActions } from '../../actions';
import { SetSubscriptionMessageHelper } from '../../helper/set-subsctiption-message.helper';
import { PaymentData } from '../../models/payment-data.model';
import { SubscriptionModel } from '../../models/subsctiption-plan.model';
import { SetSubscriptionState } from '../../states/set-subscription.state';

@Component({
  selector: 'app-payment-process',
  templateUrl: './payment-process.component.html',
  styleUrls: ['./payment-process.component.css']
})
export class PaymentProcessComponent {
  @Select(SetSubscriptionState.purchasedPlan) purchasedPlan$: Observable<SubscriptionModel>;

  constructor(private store: Store,
  private navigation: NavigationService,
  private dialog: ConfirmationDialogService ) {}

  onTokenRecieve(data: PaymentData) {
    const plan = this.store.selectSnapshot(SetSubscriptionState.purchasedPlan);
      this.store.dispatch(new SetSubscriptionActions.UpdatePaymentData(data)).subscribe(
        _ => this.store.dispatch(new SetSubscriptionActions.PurchaseSubscription(plan.id)).subscribe(
          () => this.dialog.openSimplifiedConfirmationDialog
          (SetSubscriptionMessageHelper.successPurchaseMessage(plan.name), this.navigation.goToCompanyDashboardPage.bind(this.navigation))
      ));
  }
}
