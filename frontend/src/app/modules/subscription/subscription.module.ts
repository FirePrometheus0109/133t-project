// module
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgxStripeModule } from 'ngx-stripe';
import { MaterialModule } from '../material';
import { SharedModule } from '../shared';
import { SubscriptionRoutingModule } from './subscription-routing.module';

// services
import { ViewAvailableTrialPlanListResolver } from './resolvers/set-trial-plan.resolver';
import { SubscriptionService } from './services/subsctiption.service';

// state
import { ManageSubsctiptionResolver } from './resolvers/manage-subscription.resolver';
import { ManageSubsctiptionState } from './states/manage-subscription.service';
import { SetSubscriptionState } from './states/set-subscription.state';
import { SetTrialPlanState } from './states/set-trial-plan.state';

// component
import { NgxsModule } from '@ngxs/store';
import { CommonComponentsModule } from '../common-components';
import { ConfirmationDialogComponent } from '../shared/components/confirmation-dialog.component';
import { PaymentFormComponent } from './components/payment-form/payment-form.component';
import { PaymentHistoryTableComponent } from './components/payment-history-table/payment-history-table.component';
import { PlansTableComponent } from './components/plans-table/plans-table.component';
import { StripeDataFormComponent } from './components/stripe-data-form/stripe-data-form.component';
import { ChangeBillingInformationComponent } from './containers/change-billing-information/change-billing-information.component';
import { ManageSubscriptionComponent } from './containers/manage-subscription/manage-subscription.component';
import { PaymentProcessComponent } from './containers/payment-process/payment-process.component';
import { SetSubscriptionPanelComponent } from './containers/set-subscription-panel/set-subscription-panel.component';
import { SetTrialPlanComponent } from './containers/set-trial-plan/set-trial-plan.component';

export const SUBSCTIPTION_COMPONENT = [
  PaymentProcessComponent,
  StripeDataFormComponent,
  PaymentFormComponent,
  SetTrialPlanComponent,
  PlansTableComponent,
  SetSubscriptionPanelComponent,
  ManageSubscriptionComponent,
  PaymentHistoryTableComponent,
  ChangeBillingInformationComponent
];


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MaterialModule,
    SharedModule,
    CommonComponentsModule,
    SubscriptionRoutingModule,
    NgxStripeModule.forRoot(),
    NgxsModule.forFeature([
      SetTrialPlanState,
      SetSubscriptionState,
      ManageSubsctiptionState
    ])
  ],
  declarations: SUBSCTIPTION_COMPONENT,
  exports: SUBSCTIPTION_COMPONENT,
  entryComponents: [ConfirmationDialogComponent],
  providers: [
    SubscriptionService,
    ViewAvailableTrialPlanListResolver,
    ManageSubsctiptionResolver
  ]
})
export class SubscriptionModule {
}
