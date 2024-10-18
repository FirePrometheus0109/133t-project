import { Component, OnInit } from '@angular/core';
import { Store } from '@ngxs/store';
import { NavigationService } from 'src/app/modules/core/services/navigation.service';
import { ConfirmationDialogService } from 'src/app/modules/shared/services/confirmation-dialog.service';
import { SetSubscriptionActions } from '../../actions';
import { SetSubscriptionMessageHelper } from '../../helper/set-subsctiption-message.helper';
import { PaymentData } from '../../models/payment-data.model';

@Component({
  selector: 'app-change-billing-information',
  templateUrl: './change-billing-information.component.html',
  styleUrls: ['./change-billing-information.component.css']
})
export class ChangeBillingInformationComponent implements OnInit {

  constructor(private store: Store,
  private navigation: NavigationService,
  private dialog: ConfirmationDialogService )  { }

  ngOnInit() {
  }

  onTokenRecieve(data: PaymentData) {
  this.store.dispatch(new SetSubscriptionActions.UpdatePaymentData(data)).subscribe(_ =>
    this.dialog.openSimplifiedConfirmationDialog(
      SetSubscriptionMessageHelper.successBillingInfoChange, this.onCancel.bind(this)
    ));
  }

  onCancel() {
    this.navigation.goToSubsctiptionManagePage();
  }
}
